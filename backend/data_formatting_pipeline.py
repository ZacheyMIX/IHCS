import re
import ast
import typing
import pandas as pd
import numpy as np
import datetime
from IPython.display import display
from dataprep.clean import clean_date, clean_df, clean_email, clean_address, clean_country, clean_url, clean_phone, clean_isbn, clean_text, clean_duplication

# set path to backend directory
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

formatted_df = None
 
def format_whole_dataset(df):
     """ formatted the whole dataframe 
         return: 
             @inferred_dtypes: data type detection for each column in the table | List of dictionaries (like no SQL)
             source: https://docs.dataprep.ai/user_guide/clean/clean_df.html
             "semantic": it helps users identify semantic variables (e.g., email) that are supported by DataPrep validating functions. Hence, users can later call the corresponding cleaning functions on these variables (e.g., “clean_email()”).
             "atomic": it helps users identify the basic data types that are built into Python (e.g., interger, floating, string).
             
             inferred_dtypes = 
             [{'column_name': 'Name',
             'semantic_data_type': 'string',
             'atomic_data_type': 'string'},
             ...
             {'column_name': 'Email',
             'semantic_data_type': 'URL',
             'atomic_data_type': 'string'}]
             
             @formatted_df = result of the use of clean_df, which is the first step/layer of the data formatting (that cleans table as an overall) | List of dictionaries (like no SQL)
             [{'name': 'Aishwarya Menon',
             'employee_id': '0194-826-537',
             'salary': '90000',
             'dob': '15th December, 1984',
             'join_date': '24.05.2009',
             'year_of_service': nan,
             'weight': '150 lbs',
             'address': '123 Elm St Apt 5, New York, NY 10001',
             'email': 'aishwarya.menon@g mail.com'},
             ...
             {'name': 'Ying Zhao',
             'employee_id': '0172-946-0580',
             'salary': '600K',
             'dob': '5/28/79',
             'join_date': '21-Nov-11',
             'year_of_service': nan,
             'weight': '107.5 kg',
             'address': '987 Elm Ave Apt 205, Virginia Beach, VA 23401',
             'email': 'ying.zhao@yahoo.c om'}]
 
     """ 
     inferred_dtypes, formatted_df = clean_df(df, standardize_missing_values='ignore', clean_header='const')
     inferred_dtypes = inferred_dtypes.reset_index().rename(columns={'index': 'column_name'})
     return inferred_dtypes, formatted_df
 
def send_overall_formatted_df(inferred_dtypes, formatted_df):
     """ send the inferred data types and formatted dataframe to the frontend """
     inferred_dtypes = inferred_dtypes.to_dict('records')
     formatted_df = formatted_df.to_dict('records')
     return inferred_dtypes, formatted_df
 
def minmax_yearrange_check(min_year, max_year):
     """ check min and max year gap range """    
     return bool(max_year-min_year <=99)
 
def format_name(name):
    
    # extract the title (if exists)
    title_match = re.search(r'(\bDr\.|\bPhD|\bEsq\.|\bProf\.|\bProfessor|\bMr\.|\bMrs\.|\bMs\.)', name)
    title = title_match.group(1) if title_match else None
    print('title:', title)
    comma_index = name.find(',')

    # make sure the comma found was actually a seperator (not the one at the end)
    # first name, last name, title
    if comma_index == len(name)-1:
        name = name.replace(',', '')
        comma_index = name.find(',')

    # name has comma
    if comma_index != -1:
        # clean the name format
        name = name.replace(', ', ' ')
        name = name.split(' ')
        name = list(filter(('').__ne__, name))

        # last name, first name X.
        if name[-1].find('.') != -1:
            fname = name.pop(-2)
            lname = name.pop(0)
            mname = ' '.join(name)
        else:
            # (middle name) last name, first name
            fname = name.pop(-1)
            mname = None
            if len(name) > 1:
                lname = name.pop(-1)
                mname = ' '.join(name)
            else: lname = name[0]
    else:
        # first name (middle name) last name
        name = name.split(' ')
        fname = name[0]
        mname = None
        lname = name[-1]
        if len(name) > 2:
            _ = name.pop(0)
            _ = name.pop(-1)
            mname = ' '.join(name)
    
    if fname is None: fname = ''
    if mname is None: mname = ''
    if lname is None: lname = ''
    
    if mname is None: 
        full_name = f'{fname} {lname}'
    else:
        full_name = f'{fname} {mname} {lname}'
    
    full_name += f' ({title})' if title is not None else ''
    
    return full_name

def format_data_columns(formatted_df: pd.DataFrame, columns_to_format: typing.Dict):
     """ format the columns of the dataframe 
         @columns_to_format: a dictionary of columns to format and their data type and the year format arguments if applicable
         columns_to_format = {
             'col1': {'data_type': 'datetime'},
             'col2': {'data_type': 'US_address'},
             'col3': {'data_type': 'email'},
             'col4': {'data_type': 'country'},
             'col5': {'data_type': 'url'},
             'col6': {'data_type': 'phone'},
             'col7': {'data_type': 'isbn'},
             'col8': {'data_type': 'text'},
             'col9': {'data_type': 'datetime_w_year_format', 'min_year': min_year, 'max_year': max_year}
         }
     """
     invalid_datatypes = False
     for col in columns_to_format.keys():
        data_type = columns_to_format[col]['data_type']
        if data_type == 'datetime':
            formatted_df[col] = clean_date(formatted_df, col, errors='ignore', report=True, progress=True)[f'{col}_clean']
            formatted_df[col] = pd.to_datetime(formatted_df[col])
        elif data_type == 'datetime_w_year_format':
            if minmax_yearrange_check(columns_to_format[col]['min_year'], columns_to_format[col]['max_year']):
                formatted_df[col] = clean_date(formatted_df, col, errors='ignore', report=True, progress=True)[f'{col}_clean']
                formatted_df[col] = pd.to_datetime(formatted_df[col])
                formatted_df[col] = formatted_df[col].apply(lambda x: x.replace(year=x.year-100) if x.year > columns_to_format[col]['max_year'] else x)
            else: raise Exception("The year range is too large. Please check the year format.")
        elif data_type == 'name':
            # formatted_df[col] = formatted_df[col].apply(format_name)
            continue
        elif data_type == 'Email':
                formatted_df[col] = clean_email(formatted_df, col, errors='ignore', remove_whitespace=True, report=True, progress=True)[f'{col}_clean']
        elif data_type == 'US_address':
                formatted_df[col] = clean_address(formatted_df, col, errors='ignore', report=True, progress=True)[f'{col}_clean']
        elif data_type == 'country':
                formatted_df[col] = clean_country(formatted_df, col, errors='ignore', report=True, progress=True)[f'{col}_clean']
        elif data_type == 'url':
            formatted_df[col] = clean_url(formatted_df, col, errors='ignore', report=True, progress=True)[f'{col}_clean']
        elif data_type == 'phone':
            formatted_df[col] = clean_phone(formatted_df, col, errors='ignore', report=True, progress=True)[f'{col}_clean']
        elif data_type == 'isbn':
            formatted_df[col] = clean_isbn(formatted_df, col, errors='ignore', report=True, progress=True)[f'{col}_clean']
        elif data_type == 'text':
            formatted_df[col] = clean_text(formatted_df, col, errors='ignore', report=True, progress=True)[f'{col}_clean']
        else:
            invalid_datatypes = True

     # filter for duplicate values
     formatted_df = formatted_df.drop_duplicates()
 
     return formatted_df
 
def convert_to_mln_format(formatted_df):
     """ convert the formatted dataframe to the MLN format 
     Example: (Tuple here is the term used in database referring to the rows in the table)
     Tuple t1 = {NAME: "ALICE JOHNSON", CITY: "DOTHAN", STATE: "AL", PHONE: "3347938701", SALARY: 50000, JOIN_DATE: "2024-01-12"}
     Tuple t2 = {NAME: "ALICE JOHNSON", CITY: "DOTH",   STATE: "AL", PHONE: "3347938701", SALARY: 50000, JOIN_DATE: "2024-01-12"}
     Tuple t3 = {NAME: "ALICE JOHNSON", CITY: "DOTHAN", STATE: "AL", PHONE: "3347938701", SALARY: 50000, JOIN_DATE: "2024-01-12"}
     returns [t1, t2, t3]
     """
     return formatted_df.to_dict(orient='records')
 
def get_columns_to_format():
     """ get the columns that need to be formatted from the frontend """
     pass
     # return columns_to_format
 
def main(data_path):
     global formatted_df
     """ main function to run the script """
 
     """ >>>> user confirmation to proceed with the uploaded data """
 
     # create dataframe from the uploaded file
     md_df = pd.read_csv(data_path)
 
     # format overall data
     inferred_dtypes, formatted_df = format_whole_dataset(md_df)
 
     # send to frontend
     inferred_dtypes_frontend, formatted_df_frontend = send_overall_formatted_df(inferred_dtypes, formatted_df)
     
     print(inferred_dtypes_frontend)

     return inferred_dtypes_frontend, formatted_df_frontend
 
# columns_to_format = {
#     'name': {'data_type': 'name'},
#     'dob': {'data_type': 'datetime_w_year_format', 'min_year': 1926, 'max_year': 2025}, 
#     'join_date': {'data_type': 'datetime'},
#     'email': {'data_type': 'email'},
#     'address': {'data_type': 'US_address'}
# }

def main_cont(columns_to_format):
     global formatted_df
 
     if not columns_to_format:
         final_formatted_df = formatted_df
     else:
        final_formatted_df = format_data_columns(formatted_df, columns_to_format)
        print(f'Email column: {final_formatted_df["email"]}')
 
     # send finalized formatted df to be mln processed
     final_formatted_df.to_csv('mln_files/data/final_formatted_data.csv', index=False)
     
     print(final_formatted_df.info())
     
# inferred_dtypes_frontend, formatted_df_frontend = main_1('data/Messy-Data.csv')
# main_cont(columns_to_format)
