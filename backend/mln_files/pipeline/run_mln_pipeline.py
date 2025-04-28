import subprocess
import pandas as pd
import re
from collections import defaultdict
from dateutil import parser
import os
import time

def wait_for_files(csv_path, mln_path, check_interval=5):
    print(f"Waiting for {csv_path} and {mln_path} to appear...")

    while not (os.path.exists(csv_path) and os.path.exists(mln_path)):
        time.sleep(check_interval)

    print("Both files found. Starting the pipeline...")

def clean_name(name):
    parts = re.split(r'[,\s]+', name.strip())
    parts = [p for p in parts if p]
    if len(parts) == 1:
        return parts[0], "", ""
    elif len(parts) == 2:
        return parts[0], "", parts[1]
    else:
        return parts[0], ' '.join(parts[1:-1]), parts[-1]

def clean_salary(salary):
    if pd.isna(salary):
        return None
    salary = str(salary).replace("$", "").replace(",", "").replace(" ", "").upper()
    if "K" in salary:
        return float(salary.replace("K", "")) * 1000
    try:
        return float(salary)
    except:
        return None

def clean_weight(weight):
    if pd.isna(weight):
        return None
    weight = str(weight).lower().replace("pounds", "lbs").replace("pound", "lbs")
    weight = re.sub(r"[^\d.]", "", weight)  
    if weight:
        return f"{float(weight)} lbs"
    else:
        return None

def clean_email(email):
    if pd.isna(email):
        return None
    email = str(email).replace(" ", "").replace(".c om", ".com").replace("@g mail.com", "@gmail.com")
    return email

def clean_date(date_str):
    if pd.isna(date_str):
        return None
    try:
        date = parser.parse(str(date_str), dayfirst=False, fuzzy=True)
        return date.strftime("%Y-%m-%d")
    except:
        return None

def clean_address(address):
    if pd.isna(address):
        return None
    address = address.replace("#", "Apt").replace("APT", "Apt")
    address = re.sub(r'\s+', ' ', address) 
    return address.strip()

def repair_dataframe(df):
    repaired_rows = []

    for _, row in df.iterrows():
        first_name, middle_name, last_name = clean_name(row["Name"]) if "Name" in row else ("", "", "")

        repaired_row = {
            "FirstName": first_name,
            "MiddleName": middle_name,
            "LastName": last_name,
            "EmployeeID": str(row.get("EmployeeID", "")).replace(" ", "").replace("-", "").zfill(9),
            "Salary": clean_salary(row.get("Salary")),
            "DOB": clean_date(row.get("DOB")),
            "JoinDate": clean_date(row.get("JoinDate")),
            "Year of Service": row.get("Year of Service", ""),
            "Weight": clean_weight(row.get("Weight")),
            "Address": clean_address(row.get("Address")),
            "Email": clean_email(row.get("Email")),
            "Changes": row.get("Changes", "")
        }
        repaired_rows.append(repaired_row)

    return pd.DataFrame(repaired_rows)


def csv_to_db(csv_path, db_path):
    df = pd.read_csv(csv_path, quotechar='"')
    df.reset_index(drop=True, inplace=True)
    df['id'] = df.index.map(lambda i: f"E{i}")

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

    with open(db_path, 'w') as f:
        for _, row in df.iterrows():
            eid = row['id']
            for col, pred in casing_map.items():
                if col in row and not pd.isna(row[col]):
                    val = str(row[col]).replace('"', '').strip()
                    f.write(f'{pred}({eid}, "{val}")\n')

def run_tuffy():
    print("Running Tuffy inference...")
    subprocess.run([
        "java", "-jar", "../tuffy/tuffy.jar",
        "-i", "../mln/rules.mln",
        "-e", "../mln/facts.db",
        "-r", "../mln/final.result",
        "-q", "BadName,BadID,BadSalary,BadDOB,BadJoinDate,BadYearsOfService,BadWeight,BadAddress,BadEmail",
        "-conf", "../tuffy/tuffy.conf"
    ], check=True)
    print("Tuffy run complete.")

def parse_result(result_path):
    bad_map = defaultdict(list)
    with open(result_path, 'r') as file:
        for line in file:
            match = re.match(r'(Bad\w+)\("?(E\d+)"?\)', line.strip())
            if match:
                error_type, eid = match.groups()
                bad_map[eid].append(error_type)
    return bad_map

def annotate_csv(csv_path, result_path, output_csv_path=None):
    df = pd.read_csv(csv_path)
    if 'id' not in df.columns:
        df.reset_index(drop=True, inplace=True)
        df['id'] = df.index.map(lambda i: f"E{i}")

    bad_map = parse_result(result_path)

    changes_col = []
    for idx in range(len(df)):
        eid = f"E{idx}"
        row_changes = bad_map.get(eid, [])
        changes_col.append(", ".join(row_changes) if row_changes else "")

    df["Changes"] = changes_col

    if output_csv_path:
        df.to_csv(output_csv_path, index=False)
        print(f"Final annotated CSV saved at: {output_csv_path}")

    return df.to_dict(orient="records")

def run():
    wait_for_files(
        csv_path="../data/final_formatted_data.csv",
        mln_path="../mln/user_uploaded_rules.mln"
    )

    # Step 1: Generate .db
    csv_to_db(
        csv_path="../data/final_formatted_data.csv",
        db_path="../mln/facts.db"
    )

    # Step 2: Run Tuffy inference
    run_tuffy()

    # Step 3: Annotate + Python repairs
    annotate_csv(
        csv_path="../data/Data.csv",
        result_path="../mln/final.result",
        output_csv_path="../../results/final.csv"
    )

    df_dirty = pd.read_csv("../../results/final.csv")
    df_repaired = repair_dataframe(df_dirty)
    df_repaired = df_repaired.sort_values(by="FirstName")
    df_repaired.to_csv("../../results/final_cleaned.csv", index=False)

    print("Final cleaned file saved at: ../../results/final_cleaned.csv")
    
    return df_repaired.to_dict()
