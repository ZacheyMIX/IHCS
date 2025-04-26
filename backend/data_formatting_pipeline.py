import pandas as pd
import subprocess
import re
import os
from collections import defaultdict

def load_csv(path):
    print(f"Loading CSV: {path}")
    return pd.read_csv(path)

def generate_facts_db(cleaned_df, db_path):
    print(f"Generating .db file at {db_path}")
    cleaned_df = cleaned_df.copy()
    cleaned_df.reset_index(drop=True, inplace=True)
    cleaned_df['id'] = cleaned_df.index.map(lambda i: f"E{i}")

    casing_map = {
        "Name": "HasName",
        "EmployeeID": "HasEmployeeID",
        "Salary": "HasSalary",
        "DOB": "HasDOB",
        "JoinDate": "HasJoinDate",
        "Year of Service": "HasYearsOfService",
        "Weight": "HasWeight",
        "Address": "HasAddress",
        "Email": "HasEmail",
    }

    with open(db_path, "w") as f:
        for _, row in cleaned_df.iterrows():
            eid = row["id"]
            for col, pred_name in casing_map.items():
                if col in row and not pd.isna(row[col]):
                    val = str(row[col]).replace('"', '').replace("\n", " ")
                    f.write(f'{pred_name}({eid}, "{val}").\n')

def run_tuffy(tuffy_jar, mln_file, db_file, result_file, query_preds, conf_file):
    print("Running Tuffy inference...")
    query_string = ",".join(query_preds)
    subprocess.run([
        "java", "-jar", tuffy_jar,
        "-i", mln_file,
        "-e", db_file,
        "-r", result_file,
        "-q", query_string,
        "-conf", conf_file
    ], check=True)
    print("Tuffy inference complete.")

def parse_results(result_path):
    bad_map = defaultdict(list)
    with open(result_path, "r") as f:
        for line in f:
            match = re.match(r'(Bad\w+|Weird\w+)\("?(E\d+)"?\)', line.strip())
            if match:
                error_type, eid = match.groups()
                bad_map[eid].append(error_type)
    return bad_map

def merge_changes(dirty_df, cleaned_df, bad_map):
    dirty_df = dirty_df.copy()
    cleaned_df = cleaned_df.copy()

    dirty_df.reset_index(drop=True, inplace=True)
    cleaned_df.reset_index(drop=True, inplace=True)

    changes = []

    for idx in range(len(dirty_df)):
        eid = f"E{idx}"
        dirty_row = dirty_df.iloc[idx]
        clean_row = cleaned_df.iloc[idx]

        row_changes = []

        # Field by field comparison
        for col in dirty_df.columns:
            if col in cleaned_df.columns and dirty_row[col] != clean_row[col]:
                row_changes.append(f"{col} fixed")

        # Add flagged errors from MLN/Tuffy
        if eid in bad_map:
            row_changes.extend(bad_map[eid])

        if row_changes:
            changes.append(", ".join(row_changes))
        else:
            changes.append("")

    cleaned_df["Changes"] = changes
    return cleaned_df

def save_final_outputs(cleaned_df, final_csv_path):
    print(f"Saving final output CSV at {final_csv_path}")
    cleaned_df.to_csv(final_csv_path, index=False)
    return cleaned_df.to_dict(orient="records")

if __name__ == "__main__":
    # COMMENT OUT later when using signals from Zach

    dirty_csv = "../data/Messy-Data.csv"          # Original dirty dataset
    cleaned_csv = "../data/Cleaned-Data.csv"      # Partially cleaned (Novella output)
    mln_file = "../mln/rules.mln"                 # User-uploaded MLN file

    # Output paths
    facts_db_path = "../mln/facts.db"
    tuffy_result_path = "../mln/final.result"
    final_csv_path = "../../results/final.csv"

    # Tuffy config
    tuffy_jar = "../tuffy/tuffy.jar"
    tuffy_conf = "../tuffy/tuffy.conf"
    query_preds = [
        "BadEmail", "BadDOB", "BadSalary", "BadJoinDate", "BadWeight", 
        "BadID", "BadName", "BadYearsOfService", "BadAddress", 
        "WeirdWeight", "WeirdSalary"
    ]

    # 1. Load datasets
    dirty_df = load_csv(dirty_csv)
    cleaned_df = load_csv(cleaned_csv)

    # 2. Generate facts.db
    generate_facts_db(cleaned_df, facts_db_path)

    # 3. Run Tuffy
    run_tuffy(tuffy_jar, mln_file, facts_db_path, tuffy_result_path, query_preds, tuffy_conf)

    # 4. Parse .result
    bad_map = parse_results(tuffy_result_path)

    # 5. Merge Changes (compare dirty vs cleaned + flagged errors)
    final_cleaned_df = merge_changes(dirty_df, cleaned_df, bad_map)

    # 6. Save final CSV and return dictionary
    final_dict = save_final_outputs(final_cleaned_df, final_csv_path)

    print("✅ Pipeline complete.")

    # Zach will later import this module and use final_dict directly!
