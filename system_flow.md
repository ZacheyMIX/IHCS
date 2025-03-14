IDEAS:

Data Standardizing and Formatting System:
1. uploaded dirty dataset (converted to csv) first go through the `clean_df` from `dataprep` library which will attempt to format the whole dataset and outputs a tuple of `inferred_dtypes` and `cleaned_df`
2. based on the outputted `inferred_dtypes`, system then asks the user to verify if all columns in the dataset has the correct data types and `clean_df` is supposedly the clean version of the dataset should look like.
3. if yes, then we can proceed to standardizing process. if not then, the system asks the users to identify which columns are incorrect and have automatic clean up for columns of date/time, email, country, duplicate values, phone number, text, US street address, url, ISBN numbers. if the incorrect columns are not part of the mentioned types, then have user input the desired pattern for those columns and detected the non-matching pattern values for those columns and asks the user on how to correct them.

columns params:
1. date
    - year format checkbox with max_year fill-in box
      
      info: this is needed to identify the year of the form YY that might be ambigous. 
      i.e if the range is between 1900s and 2000s and the year is 22, the system will automatically recognized it as 2022, unless this checkbox is checked.
      
      if yes, then those year 
    