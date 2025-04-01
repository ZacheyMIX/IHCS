System Flow:

Data Standardizing and Formatting System:
1. uploaded dirty dataset (converted to csv) first go through the `clean_df` from `dataprep` library which will attempt to format the whole dataset and outputs a tuple of `inferred_dtypes` and `cleaned_df`
2. based on the outputted `inferred_dtypes`, system then asks the user to verify if all columns in the dataset has the correct data types and `clean_df` is supposedly the clean version of the dataset should look like.
3. if yes, then we can proceed to standardizing process. if not then, the system asks the users to identify which columns are incorrect (sent to the backend as a dictionary where the key is the column name and the value is the datatype for their respective column) and have automatic clean up for columns of:
  - date/time, 
  - email, 
  - country, 
  - phone number (if include country code, then US only), 
  - text, 
  - US street address, 
  - url, 
  - ISBN numbers

If there are some values that are recognized as invalid parsing values, meaning they are not part of the anticipated error pattern, then the system will ask the user on how to handle the invalid parsing. Then, we can start sort out for duplicated values.

If the incorrect columns are not part of the mentioned types, then have user input the desired pattern for those columns and detected the non-matching pattern values for those columns and asks the user on how to correct them. 

If there exists any invalid parsing in the automatic clean up, then the system will accumulate the errors and asked the users on how to handle the invalid parsing.

Note on columns options:
1. date
    - `year_format` checkbox with `max_year` and `min_year` fill-in box
      
      info: this is needed to identify the year of the form YY that might be ambigous. 
      i.e if the range is between 1900s and 2000s and the year is 22, the system will automatically recognized it as 2022, unless this checkbox is checked.
      
      if the `year_format` checkbox is checked, the system will ask the user to specify the range of years that the dataset covers (the minimum(`min_year`) and maximum(`max_year`) year of the date column covers). The gap or difference between the `min_year` and `max_year` less than 100 years. If both `min_year` and `max_year` are None (no input), then it is considered an invalid input and the system will ask the user to specify the year range again. If `min_year` year has no input but the `max_year` has input, then the default value for the `min_year` is `max_year`-99 and vice versa. 
      
      For example:
      - `min_year` = 1900 and `max_year` = 2000, this will result in warning and make the user to input the correct range of years.
      - `min_year` = 1926 and `max_year` = 2025, then if YY <= 25, then YYYY = (2000-2025) and if YY > 25, then YYYY = (1926-1999). i.e YY=22 will be converted to 2022 and YY=30 will be converted to 1930.

2. Text
The default pipeline for the clean_text() function is the following: (taken from dataprep API Documentation)
  - fillna: Replace all null values with NaN.
  - lowercase: Convert all characters to lowercase.
  - remove_digits: Remove numbers.
  - remove_html Remove HTML tags.
  - remove_urls: Remove URLs.
  - remove_punctuation: Remove punctuation marks.
  - remove_accents: Remove accent marks.
  - remove_stopwords: Remove stopwords.
  - remove_whitespace: Remove extra spaces, and tabs and newlines.

<!-- The pipeline can be customized by filling in the customized pipeline box. The custom pipeline can take actions from the list above or custom functions from the user. Like the following:
```python
import re

def split(text: str) -> str:
    return str(text).split()

def replace_z(text: str, value: str) -> str:
    return re.sub(r"z", value, str(text), flags=re.I)

custom_pipeline = [
    {"operator": "lowercase"},
    {"operator": "remove_digits"},
    {"operator": split},
    {"operator": replace_z, "parameters": {"value": "*"}},
    {"operator": "remove_whitespace"},
]
``` -->