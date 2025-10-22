import yaml
import pandas as pd
from dq_engine.main_validator import run_all_rules, run_single_rule  # adapt to your names

def load_rules_yaml(path):
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return [r["name"] for r in data["rules"]]

def get_available_columns(dq_type):
    path = f"dq_engine/data/{dq_type}_data.csv"
    df = pd.read_csv(path)
    return list(df.columns)

def run_validation(data_path, yaml_path, selected_rule=None):
    if selected_rule:
        return run_single_rule(data_path, yaml_path, selected_rule)
    else:
        return run_all_rules(data_path, yaml_path)
