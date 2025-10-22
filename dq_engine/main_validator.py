import pandas as pd
import yaml
import re
from datetime import datetime

# -----------------------------
# Core Rule Functions
# -----------------------------

def one_of(series, values):
    return series.isin(values)

def not_null(series):
    return series.notnull() & (series.astype(str).str.strip() != "")

def custom_regex(series, pattern):
    return series.astype(str).str.match(pattern)

def alphanumeric(series):
    return series.astype(str).str.isalnum()

def min_length(series, min_len):
    return series.astype(str).str.len() >= min_len

def date_greater_than_today(series):
    today = pd.to_datetime(datetime.today().date())
    return pd.to_datetime(series, errors='coerce') > today

# -----------------------------
# Rule Evaluator
# -----------------------------

def evaluate_rule(df, rule):
    import numpy as np
    import pandas as pd
    import re

    if 'condition' in rule:
        cond_str = rule['condition']

        # --- CLEAN AND NORMALIZE THE CONDITION STRING ---
        cond_str = re.sub(r"\bnull\b", "None", cond_str, flags=re.IGNORECASE)
        cond_str = cond_str.replace("== None", ".isnull()")
        cond_str = cond_str.replace("!= None", ".notnull()")
        cond_str = cond_str.replace("is None", ".isnull()")
        cond_str = cond_str.replace("is not None", ".notnull()")
        cond_str = cond_str.replace("is null", ".isnull()")
        cond_str = cond_str.replace("is not null", ".notnull()")
        cond_str = cond_str.replace("== null", ".isnull()")
        cond_str = cond_str.replace("!= null", ".notnull()")
        cond_str = cond_str.replace(" and ", " & ")
        cond_str = cond_str.replace(" or ", " | ")

        try:
            condition_series = df.eval(cond_str, engine='python')
            applicable = df[condition_series]
        except Exception as e:
            print(f"[Warning] Could not parse condition: {cond_str}. Error: {e}")
            applicable = df
    else:
        applicable = df

    col = rule.get("column")

    if rule["rule"] == "one_of":
        result = applicable[col].isin(rule["value"])

    elif rule["rule"] == "not_null":
        result = applicable[col].notnull()

    elif rule["rule"] == "empty":
        result = applicable[col].isnull()

    elif rule["rule"] == "custom_regex":
        pattern = re.compile(rule["value"])
        result = applicable[col].astype(str).apply(lambda x: bool(pattern.match(x)))

    elif rule["rule"] == "alphanumeric":
        result = applicable[col].astype(str).str.isalnum()

    elif rule["rule"] == "min_length":
        result = applicable[col].astype(str).str.len() >= int(rule["value"])

    elif rule["rule"] == "date_greater_than_today":
        result = pd.to_datetime(applicable[col], errors='coerce',dayfirst=True) > pd.Timestamp.today()

    else:
        raise ValueError(f"Unknown rule type: {rule['rule']}")

    # Fill False for rows not covered by condition
    mask = pd.Series([True] * len(df), index=df.index)
    mask.loc[applicable.index] = result

    return mask


# -----------------------------
# Runner Function
# -----------------------------

def run_validation(data_path, rule_path):
    print('1')
    df = pd.read_csv(data_path)
    with open(rule_path, 'r') as f:
        rules_yaml = yaml.safe_load(f)

    results = []

    for rule in rules_yaml["rules"]:
        mask = evaluate_rule(df.copy(), rule)
        failed_rows = df[~mask]
        results.append({
            "rule": rule["name"],
            "failed_count": (~mask).sum(),
            "failed_rows": failed_rows
        })

    return results

# Run all rules
def run_all_rules(data_path, yaml_path):
    """
    Executes all rules in the YAML file on the dataset.
    Returns list of dictionaries with rule name, failed count, and failed rows.
    """
    return run_validation(data_path, yaml_path)


# Run a single rule
def run_single_rule(data_path, yaml_path, selected_rule):
    """
    Executes only the selected rule from the YAML file.
    Returns the result dict for that rule.
    """
    results = run_validation(data_path, yaml_path)
    
    # Filter only the selected rule
    for res in results:
        if res['rule'] == selected_rule:
            return [res]  # Return as list to match output format
    return []  # If rule not found
