import subprocess
import pandas as pd
import re
from collections import defaultdict

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
    with open(result_path, "r") as file:
        for line in file:
            match = re.match(r'(Bad\w+|Weird\w+)\("?(E\d+)"?\)', line.strip())
            if match:
                error_type, eid = match.groups()
                bad_map[eid].append(error_type)
    return bad_map

def annotate_csv(csv_path, result_path, output_csv_path=None):
    df = pd.read_csv(csv_path)
    if "id" not in df.columns:
        df.reset_index(drop=True, inplace=True)
        df["id"] = df.index.map(lambda i: f"E{i}")

    bad_map = parse_result(result_path)

    changes_col = []
    for idx in range(len(df)):
        eid = f"E{idx}"
        changes = ",".join(bad_map.get(eid, []))
        changes_col.append(changes)

    df["Changes"] = changes_col

    if output_csv_path:
        df.to_csv(output_csv_path, index=False)
        print(f"Final annotated CSV saved at: {output_csv_path}")

    return df.to_dict(orient="records")

if __name__ == "__main__":
    run_tuffy()
    annotate_csv(
    csv_path="../data/Messy-Data.csv",
    result_path="../mln/final.result",
    output_csv_path="../../results/final.csv"
)

