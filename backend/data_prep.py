import ast
import pandas as pd
import numpy as np
import datetime
from IPython.display import display
from dataprep.clean import clean_date, clean_df, clean_email, clean_address, clean_country, clean_url, clean_phone, clean_isbn, clean_text, clean_duplication

def main():
    
    # get the data path from the user
    data_path = input("Enter the data path")
    data_path = '/Users/novellaalvina/Documents/US/UTAH/Lessons/MS/Spring2025/CS 6964/project/IHCS/potential_dataset/Messy-Data.csv'
    
    # create dataframe from the uploaded file
    md_df = pd.read_csv(data_path)
    
    # display the few examples of the data and ask user to verify
    display(md_df.head(10))
    user_verification = str(input("Confirm to continue the process with the uploaded data? y/n ")).lower()
    while user_verification != 'y':
        data_path = input("Please enter the correct data path")
        md_df = pd.read_csv(data_path)
        display(md_df.head(10))
        user_verification = input("Comfirm to continue the process with the uploaded data? y/n")
    
    # formatted the whole dataframe first
    inferred_dtypes, formatted_df = clean_df(md_df, standardize_missing_values='ignore')
    
    # display the data info and example of the formatted data and asked the user to verify
    display(inferred_dtypes)
    display(formatted_df.head(10))
    user_verification = input("Do the formatted data look good? (y/n) ")
    
    if user_verification != 'y':
        custom_column = False
        # ask the user which columns need to be formatted and their correct datatype
        column_to_format_validation = False
        while column_to_format_validation == False:
            columns_to_format = ast.literal_eval(input("Which columns need to be formatted? (dict = {col: datatype})"))
            if not isinstance(columns_to_format, dict):
                print("The columns_to_format has to be a dictionary. Please try again.")
            else:
                column_to_format_validation = True
        
        # columns_to_format = {'dob': 'datetime', 'join_date': 'datetime', 'email': 'email', 'address': 'US_address'}
        # columns_to_format = columns_to_format.split(',')
        # columns_to_format = [col.strip() for col in columns_to_format]
       
        # year format checking
        year_format_validation = False
        while not year_format_validation:
            year_format = ast.literal_eval(input("Which columns need to format the year? (dict = {col: {'min': year, 'max': year}})"))
            if not isinstance(year_format, dict):
                print("The year_format has to be a dictionary. Please try again.")
                break
            # year_format = {'dob': {'min': 1926, 'max': 2025}} # only dob column needs formatting
        
            for col in year_format.keys():
                min_year = year_format[col]['min']
                max_year = year_format[col]['max']
                
                # check for the min and max year null values
                if min_year is None or max_year is None: break                          # if both min and max year are none, then ask the user to input again
                if min_year is None and max_year is not None: min_year = max_year - 99  # if the min year is None but the max year is not None, then the min year will be 99 years less than the max year.
                if max_year is None and min_year is not None: max_year = min_year + 99  # if the max year is None but the min year is not None, then the max year will be 99 years more than the min year.
                
                # if the gap between min and max year is greater than or equal to 100, then ask the user to input again
                if max_year - min_year >= 100:
                    year_format = ast.literal_eval(input(f"The {col} year range is too large. Please check the year format. Please enter the correct year range. \nWhich columns need to format the year? (dict = {col: {'min': year, 'max': year}})"))
                    break
                
                # if the col is the last column with no 'break', then the year format is valid
                if col == list(year_format.keys())[-1]: year_format_validation = True
        
        """
        # # text custom pipeline checking
        # pipeline_validation = False
        # while not pipeline_validation:
        #     pipeline_message = f'Customize your text cleaning pipeline following the template in the README.'
        #     custom_pipeline = input(pipeline_message)
        #     custom_pipeline = [
        #         {"operator": "lowercase"},
        #         {"operator": "remove_digits"},
        #         {"operator": split},
        #         {"operator": replace_z, "parameters": {"value": "*"}},
        #         {"operator": "remove_whitespace"},
        #     ]
            
        #     # check if the custom pipeline follows the template given
        #     if not isinstance(custom_pipeline, list):
        #         print("The custom pipeline has to be wrapped in a list as shown in the template. Please try again.")
        #         break
        #     else:
        #         for op in custom_pipeline:
        #             op = ast.literal_eval(op)
        #             if not isinstance(op, dict):
        #                 print("Each operator in the custom pipeline has to be wrapped in a dictionary as shown in the template. Please try again.")
        #                 break
        #             else:
        """            
        
        error_list = [] 
        for col in columns_to_format.keys():
            data_type = columns_to_format[col]
            try:
                if data_type == 'datetime':
                    formatted_df[col] = clean_date(formatted_df, col, errors='raise', report=True, progress=True)[f'{col}_clean']
                    formatted_df[col] = pd.to_datetime(formatted_df[col])
                    if year_format[col]:
                        formatted_df[col] = formatted_df[col].apply(lambda x: x.replace(year=x.year-100) if x.year > year_format[col]['max'] else x)
                elif data_type == 'email':
                    formatted_df[col] = clean_email(formatted_df, col, errors='raise', remove_whitespace=True, report=True, progress=True)[f'{col}_clean']
                elif data_type == 'US_address':
                    formatted_df[col] = clean_address(formatted_df, col, errors='raise', report=True, progress=True)[f'{col}_clean']
                elif data_type == 'country':
                    formatted_df[col] = clean_country(formatted_df, col, errors='raise', report=True, progress=True)[f'{col}_clean']
                elif data_type == 'url':
                    formatted_df[col] = clean_url(formatted_df, col, errors='raise', report=True, progress=True)[f'{col}_clean']
                elif data_type == 'phone':
                    formatted_df[col] = clean_phone(formatted_df, col, errors='raise', report=True, progress=True)[f'{col}_clean']
                elif data_type == 'isbn':
                    formatted_df[col] = clean_isbn(formatted_df, col, errors='raise', report=True, progress=True)[f'{col}_clean']
                elif data_type == 'text':
                    formatted_df[col] = clean_text(formatted_df, col, errors='raise', report=True, progress=True)[f'{col}_clean']
                else:
                    custom_column = True
                
            except Exception as error:
                error_list.append(error.__str__)
        
        # filter for duplicate values
        formatted_df = formatted_df.drop_duplicates()
        
        # going through every invalid parsing
        for err in error_list:
            print(err)
            
                
if __name__ == '__main__':
    main()
