# Integrated Hybrid Cleaning System (IHCS)

Data cleaning is a critical prerequisite for accurate data analysis, yet it is often time-consuming and error-prone.

We present IHCS, an integrated hybrid data cleaning system that automates error detection and repair by combining probabilistic inference with deterministic field-level corrections.

In the preprocessing stage, IHCS monitors for incoming user uploads, formats the input dataset, and transforms user-provided data quality rules into a unified MLN (Markov Logic Network) format. The system then runs probabilistic error detection using Tuffy and flags abnormalities based on learned relationships. After detection, IHCS applies targeted field repairs through Python-based standardization, dynamically interpreting flagged errors without requiring manual intervention.

The visual interface allows users to upload datasets and rules, monitor the cleaning process, and view the final cleaned results both as downloadable files and through dynamic frontend visualization. Users can also see how well the system performed through evaluation metrics (runtime, precision, recall, and F1 score) displayed on the screen.

This project was built as part of the CS 4964/CS 6964: Manage Data for & with ML course at the University of Utah.

###Reference: 

- **Paper:** [Original IHCS Paper (VLDB 2019)](https://www.vldb.org/pvldb/vol12/p1874-ge.pdf).
- **Tuffy:** [Tuffy Source](https://github.com/HazyResearch/tuffy.git).

---

## Installation Instructions

### 1. Clone this repository
```
git clone https://github.com/ZacheyMIX/IHCS.git
cd IHCS
```
### 2. Set up the Python Enviornment
```
conda env create -f environment.yml -n ihcs
conda activate ihcs
```
To update the environment later:
```
conda env update --file environment.yml
```
### 3. Install PostgreSQL

- Install PostgreSQL (recommended version: 14 or compatible).
- Open pgAdmin and create a new database named:
```
tuffydb
```
### 3. Configure tuffy.conf

- Navigate to backend/mln_files/tuffy/.
- Edit the tuffy.conf file:
```
db_url = jdbc:postgresql://localhost:5432/tuffydb
db_username = <your_pgadmin_username>
db_password = <your_pgadmin_password>
dir_working = C:/Users/<your_username>/Desktop/IHCS/backend/mln_files/tuffy/temp
```
- **Important:** Make sure PostgreSQL is running before starting IHCS.

### 4. Java Requirement

- Make sure Java (version 8 or higher) is installed.

---

## How IHCS Works

### Frontend:

- **User uploads:**

    - A .csv dirty dataset.
    - A .mln file specifying data quality rules.

### Backend Pipeline:

- Detects new uploads automatically.
- Formats the uploaded dataset partially using Dataprep.
- Converts the formatted dataset into a .db facts file.
- Runs MLN-based probabilistic error detection using Tuffy.
- Repairs erroneous fields automatically with Python-based logic.
- Evaluates cleaning performance using F1 score, precision, and recall.

### Outputs:

- A cleaned .csv file.
- A .json file for dynamic frontend visualization.

### Visual Interface:

- Shows cleaned data along with an added "changes" column that lists all error repairs for transparency.
- Also displays evaluation metrics, including runtime, precision, recall, and F1 score.

---

## Important Notes

- The system automatically monitors the data/ and mln/ folders.
- Uploading new files automatically triggers the backend cleaning process, no manual restart needed.
- A prompt guides users on how to structure their .mln rule files correctly.
- PostgreSQL server must be running whenever IHCS is active.
