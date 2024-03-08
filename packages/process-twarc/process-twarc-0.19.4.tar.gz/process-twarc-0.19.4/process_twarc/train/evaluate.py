import sqlite3
import pandas as pd
from pandas import ExcelWriter
from process_twarc.util import load_dict
from process_twarc.train.util import load_datasets, get_compute_metrics
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer
import os
from tqdm import tqdm
import torch
import shutil

def get_data(path_to_db: str) -> dict:
    """Get data from an SQL database and return a dictionary of DataFrames."""

    def query(
        path_to_db: str,
        table_name: str,
        column_names: list=None
    ) -> pd.DataFrame:
        """Query an SQL database and return a Pandas DataFrame."""
        
        conn = sqlite3.connect(path_to_db)
        c = conn.cursor()
        
        if column_names is None:
            c.execute(f"SELECT * FROM {table_name}")
            column_names = [description[0] for description in c.description]
        else:
            # Validate column names to make sure they're properly formatted
            if not all(isinstance(col, str) for col in column_names):
                print("Error: All column names must be strings.")
                return None
        
        column_names_str = ", ".join(column_names)
        c.execute(f"SELECT {column_names_str} FROM {table_name}")
        
        rows = c.fetchall()
        df = pd.DataFrame(rows, columns=column_names)
        
        conn.close()
        
        return df

    queries = {
    "studies": [
        "study_id",
        "study_name"
    ],
    "study_directions": [
        "direction",
        "study_id"
    ],
    "trials": [
        "trial_id",
        "number",
        "study_id",
        "state"
    ],
    "trial_values": [
        "trial_id",
        "value"
    ],
    "trial_intermediate_values": [
        "trial_id",
        "step"
    ],
    "trial_params": [
        "trial_id",
        "param_name",
        "param_value"
    ]
    }
    
    data = {}
    for table_name, column_names in queries.items():
        data[table_name] = query(path_to_db, table_name, column_names)
    
    return data


def get_run_name(row):
    trial = f"trial-{str(row['number']+1).zfill(3)}"
    return f"{row['study_name']}/{trial}"

def get_epochs(trial_intermediate_values):
    trial_id2epoch = {}
    for group, df in trial_intermediate_values.groupby("trial_id"):
        trial_id2epoch[group] = len(df)
    return trial_id2epoch

def get_params(trial_params):
    trial_id2params = {}
    for group, df in trial_params.groupby("trial_id"):
        trial_id2params[group] = df.set_index("param_name")["param_value"].to_dict()
    return trial_id2params

def unpack_params(row):
    params = row["params"]
    for param, value in params.items():
        row[param] = value
    return row

def generate_summary_table(
    path_to_db: str,
    n_best_trials: int=int(),
    path_to_output: str=None
    ):
    """Generate a summary table of the best trials from an SQL database."""

    print("Generating summary table.")
    data = get_data(path_to_db)
    trial_values = data["trial_values"]
    trial_values = trial_values.merge(data["trials"], on="trial_id")
    trial_values = trial_values.merge(data["studies"], on="study_id")
    trial_values = trial_values.merge(data["study_directions"], on="study_id")
    trial_values = trial_values[trial_values["state"] == "COMPLETE"]
    trial_values["epochs"] = trial_values["trial_id"].map(get_epochs(data["trial_intermediate_values"]))
    trial_values["params"] = trial_values["trial_id"].map(get_params(data["trial_params"]))
    trial_values = trial_values.apply(unpack_params, axis=1)
    trial_values["run_name"] = trial_values.apply(get_run_name, axis=1)
    #make a dictionary of trial values where the key is the study name
    trial_values = {group: df for group, df in trial_values.groupby("study_name")}

    if n_best_trials:
        print(f"Trimming to best trials. {n_best_trials=}")
        best_trials = {}
        for group, df in trial_values.items():
            direction = df["direction"].iloc[0]
            if direction == "MAXIMIZE":
                ascending=False
            else:
                ascending=True

            df = df.sort_values("value", ascending=ascending)[:n_best_trials].reset_index(drop=True)
            best_trials[group] = df
        trial_values = best_trials

    if path_to_output:
        print(f"Saving to {path_to_output}.")
        with ExcelWriter(path_to_output) as writer:
            for study_name, df in trial_values.items():
                if "/" in study_name:
                    study_name = study_name.split("/")[-1]
                df.to_excel(writer, sheet_name=study_name, index=False)
    
    return trial_values

def check_results(
    path_to_best_trials: str,
    path_to_config: str,
    splits_dir: str,
    groups: list=None
):
    
    config = load_dict(path_to_config)
    fixed_parameters = config["fixed_parameters"]
    completed_dir = fixed_parameters["completed_dir"]
    if not groups:
        groups = list(config["group_parameters"].keys())
    best_trials = {group: pd.read_excel(path_to_best_trials, sheet_name=group) for group in groups}


    for group, df in best_trials.items():
        group_parameters = config["group_parameters"][group] if "group_parameters" in config.keys() else {}
        parameters = {**fixed_parameters, **group_parameters}

        get_ = lambda param: parameters[param] if param in parameters.keys() else None
  
        tokenizer = AutoTokenizer.from_pretrained(parameters["path_to_model"])
        datasets = load_datasets(
            data_dir=splits_dir,
            splits = ["development", "test"],
            tokenizer=tokenizer,
            label_column=get_("label_column"),
        )

        compute_metrics = get_compute_metrics(parameters)

        new_df = df

        for idx, row in tqdm(df.iterrows(), desc=f"Checking {group}"):

            project = get_("project")
            path_to_model = os.path.join(completed_dir, project, row["run_name"])
            if os.path.exists(path_to_model):

                training_args = torch.load(os.path.join(path_to_model, "training_args.bin"))
                training_args.report_to = "none"
                torch.save(training_args, os.path.join(path_to_model, "training_args.bin"))
                model = AutoModelForSequenceClassification.from_pretrained(path_to_model)

                trainer = Trainer(
                    model=model,
                    tokenizer=tokenizer,
                    compute_metrics=compute_metrics
                )


                dev_metric, test_metric = get_("metric_for_best_trial"), get_("metric_for_best_results")
                results = lambda split, metric: trainer.evaluate(datasets[split])[metric]


                new_df.at[idx, "dev_results"] = results("development", dev_metric)
                new_df.at[idx, "test_results"] = results("test", test_metric)
            else:
                new_df = new_df.drop(idx)
        new_df["dev_equals_value"] = new_df["dev_results"] == new_df["value"]
        best_trials[group] = new_df
        with ExcelWriter(path_to_best_trials) as writer:
            for group, df in best_trials.items():
                df.to_excel(writer, sheet_name=group, index=False)
    return best_trials


def copy_best_trials(
        path_to_results: str,
        completed_dir: str,
        best_trials_dir: str,
        n_best_trials: int=int(),
        metric_for_best_results: str="test_results"
):

    best_trials = pd.read_excel(path_to_results, sheet_name=None)
    #iterate through sheets
    for _, df in best_trials.items():
        if n_best_trials:
            direction = df["direction"].iloc[0]
            if direction == "MAXIMIZE":
                ascending=False
            else:
                ascending=True
            df = df.sort_values(metric_for_best_results, ascending=ascending)[:n_best_trials].reset_index(drop=True)

        for _, row in df.iterrows():
            run_name = row["run_name"]
            source_path = os.path.join(completed_dir, run_name)
            dest_path = os.path.join(best_trials_dir, run_name)
            if os.path.exists(source_path):
                if not os.path.exists(dest_path):
                    shutil.copytree(source_path, dest_path)
                else:
                    print(f"Destination directory {dest_path} already exists. Skipping...")
            else:
                print(f"Source directory {source_path} does not exist. Skipping...")


