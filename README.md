# IHCS

Data cleaning is a prerequisite to subsequent data analysis, and is know to often be time-consuming and labor-intensive. We present IHCS, a hybrid data cleaning system that integrates error detection and repair to contend effectively with multiple error types. In a preprocessing step that precedes the data cleaning, IHCS formats an input dataset to be cleaned, and transforms applicable data quality rules into a unified format. Then, an MLNindexstructure is formed according to the unified rules, enabling IHCS to handle multiple error types simultaneously. During the cleaning, IHCS first tackles abnormalities through an abnormal group process, and then, it generates multiple data versions based on the MLN index. Finally, IHCS eliminates conflicting values across the multiple versions, and derives the final unified clean data. A visual interface enables cleaning process monitoring and cleaning result analysis.

This project is made for Data Management and/for Machine Learning at the University of Utah.  All rights reserved to the original creators of IHCS, to learn more find out here: https://www.vldb.org/pvldb/vol12/p1874-ge.pdf

## Installation
Navigate your working directory to this repo folder (IHCS):
1. create conda environment using the environment.yml we provided:
```
conda env create -f environment.yml -n ihcs
```

2. activate the conda environment
```
conda activate ihcs
```
3. add new packages to environment.yml, to update it in conda:
```
conda env update --file environment.yml
```
and restart your IDE.