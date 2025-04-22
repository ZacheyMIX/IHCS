import pandas as pd
import subprocess
import argparse
import os
import shutil
import re


def extract_used_predicates(mln_path):
    with open(mln_path, "r") as f:
        lines = f.readlines()
    preds = set()
    for line in lines:
        matches = re.findall(r"Has\w+", line)
        preds.update(matches)
    return preds


def csv_to_db(csv_path, db_path, used_preds):
    df = pd.read_csv(csv_path)
    df.reset_index(drop=True, inplace=True)
    df["id"] = df.index.map(lambda i: f"E{i}")  
    casing_map = {
        "EmployeeID": "HasEmployeeID",
        "Name": "HasName",
        "Salary": "HasSalary",
        "DOB": "HasDOB",
        "JoinDate": "HasJoinDate",
        "Year of Service": "HasYearsOfService",
        "Weight": "HasWeight",
        "Address": "HasAddress",
        "Email": "HasEmail",
    }
    with open(db_path, "w") as f:
        for index, row in df.iterrows():
            eid = row["id"]
            for col in df.columns:
                if col == "id":
                    continue
                pred_name = casing_map.get(col, "Has" + col.title().replace(" ", ""))
                if pred_name not in used_preds:
                    continue
                value = str(row[col]).replace('"', "\"")
                f.write(f'{pred_name}({eid}, "{value}")\n')
    df.to_csv(csv_path, index=False)  


def save_mln_rules(rules_str, mln_path):
    with open(mln_path, "w") as f:
        f.write(rules_str.strip() + "\n")


def run_tuffy(tuffy_path, mln_file, db_file, result_file, query_preds, conf_path):
    query_string = ",".join(query_preds)
    command = [
        "java", "-jar", tuffy_path,
        "-i", mln_file,
        "-e", db_file,
        "-r", result_file,
        "-q", query_string,
        "-conf", conf_path
    ]
    subprocess.run(command, check=True)


def parse_results(result_path):
    changes = {}
    with open(result_path, "r") as f:
        for line in f:
            if "(" in line:
                prob, pred = line.strip().split(None, 1) if line[0].isdigit() else (None, line.strip())
                pred_name, args = pred.split("(")
                entity = args.split(",")[0].strip().replace('"', '')
                changes.setdefault(entity, []).append(pred_name)
    return changes


def apply_flags_to_csv(csv_path, changes_dict, output_path):
    df = pd.read_csv(csv_path)
    df["changes"] = df["id"].apply(lambda eid: changes_dict.get(eid, None))
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Path to cleaned CSV")
    parser.add_argument("--rules", required=True, help="MLN rules as a string or path to file")
    parser.add_argument("--tuffy", default="../tuffy/tuffy.jar", help="Path to tuffy.jar")
    parser.add_argument("--conf", default="../tuffy/tuffy.conf", help="Path to tuffy.conf")
    args = parser.parse_args()


    if os.path.isfile(args.rules):
        with open(args.rules, "r") as f:
            args.rules = f.read()

    # Paths
    mln_file = "../notebook/mln/user_rules.mln"
    db_file = "../notebook/mln/user_facts.db"
    result_file = "../notebook/mln/messy.result"
    final_csv_path = "../../results/final_output.csv"
    query_preds = ["BadEmail", "WeirdWeight", "WeirdSalary"]

    # Save rules and extract used predicates
    save_mln_rules(args.rules, mln_file)
    used_preds = extract_used_predicates(mln_file)

    # Generate DB only using valid predicates
    csv_to_db(args.csv, db_file, used_preds)

    # Run tuffy and parse results
    run_tuffy(args.tuffy, mln_file, db_file, result_file, query_preds, args.conf)
    changes = parse_results(result_file)
    apply_flags_to_csv(args.csv, changes, final_csv_path)

    print(f"Final cleaned file with flags saved to: {final_csv_path}")
