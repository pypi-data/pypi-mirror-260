from unicodeblock.blocks import of as block
import pandas as pd
import json
from transformers import pipeline
from collections import Counter
from process_twarc.util import load_dataset, get_output_path
import os

def get_blocks(token):
    token = token.replace("##", "")

    return ", ".join(list(set([block(char) if block(char) else "none" for char in token])))

def get_new_vocab(tokenizers):
    vocab = lambda tok: set(tok.vocab.keys())
    old_tok = tokenizers["old_tok"]

    result = {}
    for name, tokenizer in tokenizers.items():
        if name == "old_tok":
            continue
        new_tok = tokenizer
        new_vocab = vocab(new_tok) - vocab(old_tok)

        df = pd.DataFrame({"token": list(new_vocab)})
        df["blocks"] = df["token"].apply(get_blocks)

        whitelist = [
            "HIRAGANA",
            "KATAKANA",
            "CJK",
            "LATIN",
            "NUM",
            "DIGIT"
        ]
        #filter for rows where any member of the whitelist is present in blocks
        df = df[df["blocks"].str.contains("|".join(whitelist))]
        df["tok_encoding"] = df["token"].apply(lambda x: new_tok.vocab[x])
        result[name] = df
    return result

def find_target_tokens(target_tokens, pos_tokens):

    pos_tokens = list(enumerate(pos_tokens))
    target_tokens = list(target_tokens)
    result = {}

    for target in target_tokens:
    
    
        start = target[0]
        end = target[-1]
        starts = [(idx, token) for (idx, token) in pos_tokens if token.startswith(start)]
        ends = [(idx, token) for (idx, token) in pos_tokens if token.endswith(end)]

        spans = []
        for (idx1, _) in starts:
            for (idx2, _) in ends:
                if idx2 > idx1:
                    spans.append((idx1, idx2))

        #join tokens with ## stripped, if any
        get_word = lambda span: "".join([tok.replace("##", "") for (_, tok) in pos_tokens[span[0]:span[1]+1]])
        get_subwords = lambda span: {idx: {"token": pos_tokens[idx][1]} for idx in range(span[0], span[1]+1)}
        
        entries = {str(span): 
                  {
                      "word": get_word(span), 
                      "subwords": get_subwords(span)
                      } for span in spans if get_word(span) == target}
        result.update(entries)
                 
                
    return result

def get_pos_columns(dataset, tokenizers, model):
    tokenizer = tokenizers["old_tok"]

    dataset["pos_tokens"] = dataset["text"].apply(lambda x: tokenizer.tokenize(x))
    pos = pipeline("token-classification", model=model, tokenizer=tokenizer, device="cuda")
    dataset["pos_scores"] = dataset["text"].apply(lambda x: pos(x))
    return dataset

def get_target_ids(dataset, tokenizers, model):
    new_vocab = get_new_vocab(tokenizers)
    dataset = get_pos_columns(dataset, tokenizers, model)
    for name, vocab in new_vocab.items():
        tokenizer = tokenizers[name]
        dataset[f"{name}_input_ids"] = dataset["text"].apply(lambda x: tokenizer(x)["input_ids"])
        target = vocab["tok_encoding"].values
        dataset[f"{name}_target_ids"] = dataset[f"{name}_input_ids"].apply(lambda x: [i for i in x if i in target]) 
        dataset[f"{name}_target_tokens"] = dataset[f"{name}_target_ids"].apply(lambda x: [tokenizer.decode([i]) for i in x])

        targets = lambda row: find_target_tokens(row[f"{name}_target_tokens"], row["pos_tokens"])
        dataset[f"{name}_targets"] = dataset.apply(lambda x: json.dumps(targets(x), ensure_ascii=False), axis=1)
    return dataset

from collections import Counter

def combine_dicts(dict_list):
    return dict(sum((Counter(d) for d in dict_list), Counter()))


def compile_pos_results(dataset: pd.DataFrame, tokenizers: dict, model: object):
    dataset = get_target_ids(dataset, tokenizers, model)


    def dumps(idx, name, x):
        dataset.at[idx, f"{name}_result"] = json.dumps(x, ensure_ascii=False)
    
    for idx1, row in dataset.iterrows():
        for name, _ in tokenizers.items():
            tags = {
                    (s["index"]):{
                        "word": s["word"],
                        "pos_score": {s["entity"]: 1},
                    } for s in row["pos_scores"]
                } if row["pos_scores"] else {}
            
            if name == "old_tok":
                tokens = list(enumerate(row["pos_tokens"]))
                result = {
                    tup[0]: {
                        "word": tup[1],
                        "pos_score": tags.get(tup[0]+1, {"pos_score": None})["pos_score"] if tags else {"pos_score": None},
                        "group": "old_vocab"
                        } for tup in tokens
                }

                dumps(idx1, name, result)
                
            else:
                targets = json.loads(row[f"{name}_targets"])

                result = {} 
                for span in targets.keys():
                    word = targets[span]
                    subwords = word["subwords"]
                
                    for idx2 in subwords:
                        subword = subwords[idx2]
                        pos_score = tags.pop(int(idx2)+1, {"pos_score": None}) if tags else {"pos_score": None}
                        subword["pos_score"] = pos_score["pos_score"]    

                    #get all_scores by creating a dictionary of all pos_scores, then summing the values for each key
                        
                    all_scores = [subword["pos_score"] for subword in subwords.values() if subword["pos_score"]]
                    if all_scores:
                        all_scores = combine_dicts(all_scores)


                    word["pos_score"] = all_scores
                    word["group"] = "new_vocab"
                    result[span] = word
                
                if tags:
                    for idx3 in tags.keys():

                        old_word = {idx3: {
                            "word": tags[idx3]["word"],
                            "pos_score": tags[idx3]["pos_score"],
                            "group": "old_vocab"
                        }
                        }
                        result.update(old_word)
                
                dumps(idx1, name, result)
    return dataset

def tabulate_results(dataset, tokenizers):
    output = {}
    for name, _ in tokenizers.items():
        
        result = [json.loads(x) for x in dataset[f"{name}_result"]]
        dataset[f"{name}_result"] = result
        result = dataset[f"{name}_result"].apply(pd.Series).stack().to_frame().reset_index()
        get_column = lambda col: result[0].apply(lambda x: x[col] if col in x else None)

        result["word"] = get_column("word")
        result["pos_score"] = get_column("pos_score")
        result["group"] = get_column("group")

        combined_scores = {}
        for word in (list(set(result["word"].tolist()))):
            all_scores = result[result["word"] == word]["pos_score"].tolist()
            combined_scores[word] = combine_dicts(all_scores)
    
        result = result.groupby(["word", "group"]).size().reset_index(name="count")
        result["pos_score"] = result["word"].apply(lambda x: combined_scores[x])
        
        output[name] = result.reset_index()
    return output

def process(path_to_dataset, tokenizers, model, output_dir):
    dataset = load_dataset(
        path_to_dataset,
        columns = ["tweet_id", "text"],
        masks = ["duplicate", "pattern", "user_cap"])
    dataset = compile_pos_results(dataset, tokenizers, model)
    output = tabulate_results(dataset, tokenizers)

    intermediate_dir = f"{output_dir}/intermediate"
    pos_tags_dirs = {name: f"{output_dir}/pos_tags_{name}" for name in tokenizers.keys()}
    for dir in list(pos_tags_dirs.values()) + [intermediate_dir]:
        os.makedirs(dir, exist_ok=True)
    
    dataset.to_parquet(get_output_path(path_to_dataset, intermediate_dir))
    for name, df in output.items():
        df.to_parquet(get_output_path(path_to_dataset, pos_tags_dirs[name]))

    return dataset, output