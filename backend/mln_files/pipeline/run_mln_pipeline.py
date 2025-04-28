import subprocess
import pandas as pd
import re
from collections import defaultdict
from dateutil import parser
import os
import time
import shutil

# Wait for new uploads in the folders (csv = data, mln = rules)
def wait_for_new_upload(csv_folder, mln_folder, check_interval=5):
    print(f"Waiting for new uploads in {csv_folder} and {mln_folder}...")

    last_csv_mtime = None
    last_mln_mtime = None

    while True:
        csv_files = [f for f in os.listdir(csv_folder) if f.endswith(".csv")]
        mln_files = [f for f in os.listdir(mln_folder) if f.endswith(".mln")]

        if csv_files and mln_files:
            csv_path = os.path.join(csv_folder, csv_files[0])
            mln_path = os.path.join(mln_folder, mln_files[0])

            csv_mtime = os.path.getmtime(csv_path)
            mln_mtime = os.path.getmtime(mln_path)

            if (last_csv_mtime != csv_mtime) or (last_mln_mtime != mln_mtime):
                last_csv_mtime = csv_mtime
                last_mln_mtime = mln_mtime
                print("New upload detected!")
                return csv_path, mln_path

        time.sleep(check_interval)

def clean_name(name):
    titles = {"Mr.", "Mrs.", "Ms.", "Dr.", "Prof.", "Professor", "PhD", "Esq.", "Esq", "MD", "Miss"}
    if pd.isna(name):
        return "", "", "", ""

    name = str(name).strip()

    if "," in name:
        parts = [p.strip() for p in name.split(",")]
        if len(parts) == 2:
            last, first_middle = parts
            first_middle_parts = first_middle.split()
            if len(first_middle_parts) == 1:
                return first_middle_parts[0], "", last, ""
            elif len(first_middle_parts) == 2:
                return first_middle_parts[0], first_middle_parts[1], last, ""
            elif len(first_middle_parts) >= 3:
                return first_middle_parts[0], " ".join(first_middle_parts[1:-1]), last, first_middle_parts[-1]
        elif len(parts) == 3:
            last, title, first = parts
            return first, "", last, title
        
    parts = name.split()
    title = ""
    if parts and parts[0] in titles:
        title = parts[0]
        parts = parts[1:]

    if len(parts) == 1:
        return parts[0], "", "", title
    elif len(parts) == 2:
        return parts[0], "", parts[1], title
    elif len(parts) == 3:
        return parts[0], parts[1], parts[2], title
    elif len(parts) >= 4:
        return parts[0], parts[1], " ".join(parts[2:]), title
    else:
        return "", "", "", title


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
    return f"{float(weight)} lbs" if weight else None

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

# Actually run Tuffy
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
    print("Tuffy inference done!")

# Parse Tuffy results into a dictionary
def parse_result(result_path):
    bad_map = defaultdict(list)
    with open(result_path, 'r') as file:
        for line in file:
            match = re.match(r'(Bad\w+)\("?(E\d+)"?\)', line.strip())
            if match:
                error_type, eid = match.groups()
                bad_map[eid].append(error_type)
    return bad_map

# Mark bad rows in the CSV
def annotate_csv(csv_path, result_path):
    df = pd.read_csv(csv_path)
    if 'id' not in df.columns:
        df.reset_index(drop=True, inplace=True)
        df['id'] = df.index.map(lambda i: f"E{i}")

    bad_map = parse_result(result_path)

    changes_col = []
    for idx in range(len(df)):
        eid = f"E{idx}"
        changes = bad_map.get(eid, [])
        changes_col.append(", ".join(changes) if changes else "")

    df["Changes"] = changes_col
    return df

def format_employee_id(empid):
    if pd.isna(empid):
        return ""
    empid = re.sub(r"[^\d]", "", str(empid))  
    if len(empid) == 9:
        return f"{empid[:4]}-{empid[4:7]}-{empid[7:]}"
    elif len(empid) == 10:
        return f"{empid[:4]}-{empid[4:7]}-{empid[7:]}"
    else:
        return empid  
    
# Cleaning
def repair_dataframe(df):
    repaired_rows = []
    for idx, row in df.iterrows():
        first_name, middle_name, last_name, title = clean_name(row["Name"]) if "Name" in row else ("", "", "", "")
        repaired_row = {
            "First Name": first_name,
            "Middle Name": middle_name,
            "Last Name": last_name,
            "Title": title,
            "EmployeeID": format_employee_id(row.get("EmployeeID", "")),
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

    df_clean = pd.DataFrame(repaired_rows)
    df_clean = df_clean.sort_values(by="First Name").reset_index(drop=True)
    df_clean.index.name = ""
    return df_clean

# Clean any old .csv and .mln files if leftover
def cleanup_old_files():
    print("Cleaning old uploads...")
    for folder in ["../data/", "../mln/"]:
        for file in os.listdir(folder):
            if file.endswith(".csv") or file.endswith(".mln"):
                os.remove(os.path.join(folder, file))

def run_pipeline_once():
    cleanup_old_files()

    csv_path, mln_path = wait_for_new_upload(
        csv_folder="../data/",
        mln_folder="../mln/"
    )

    csv_to_db(csv_path, db_path="../mln/facts.db")
    run_tuffy()

    df_dirty = annotate_csv(csv_path, "../mln/final.result")

    df_repaired = repair_dataframe(df_dirty)

    # Save as CSV
    df_repaired.to_csv("../../results/final_cleaned.csv", index=True)

    # Save as JSON 
    df_repaired.to_json("../../results/final_cleaned.json", orient="records", indent=2)

    print("Final repaired dataset saved at: ../../results/final_cleaned.csv and final_cleaned.json")

def main():
    while True:
        run_pipeline_once()

if __name__ == "__main__":
    main()
