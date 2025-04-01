import ast
import typing
import pandas as pd
import numpy as np
import datetime
from IPython.display import display
from dataprep.clean import clean_date, clean_df, clean_email, clean_address, clean_country, clean_url, clean_phone, clean_isbn, clean_text, clean_duplication

def format_whole_dataset(df):
    """ formatted the whole dataframe """ 
    inferred_dtypes, formatted_df = clean_df(df, standardize_missing_values='ignore', clean_header='const')
    return inferred_dtypes, formatted_df

def minmax_yearrange_check(min_year, max_year):
    """ check min and max year gap range """    
    return bool(max_year-min_year <=99)

def format_data_columns(df: pd.DataFrame, columns_to_format: typing.Dict):
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
    
    error_list = [] 
    for col in columns_to_format.keys():
        data_type = columns_to_format[col]['data_type']
        try:
            if data_type == 'datetime':
                formatted_df[col] = clean_date(formatted_df, col, errors='raise', report=True, progress=True)[f'{col}_clean']
                formatted_df[col] = pd.to_datetime(formatted_df[col])
            elif data_type == 'datetime_w_year_format':
                if minmax_yearrange_check(columns_to_format[col]['min_year'], columns_to_format[col]['max_year']):
                    formatted_df[col] = clean_date(formatted_df, col, errors='raise', report=True, progress=True)[f'{col}_clean']
                    formatted_df[col] = pd.to_datetime(formatted_df[col])
                    formatted_df[col] = formatted_df[col].apply(lambda x: x.replace(year=x.year-100) if x.year > columns_to_format[col]['max'] else x)
                else: raise Exception("The year range is too large. Please check the year format.")
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
    
    return formatted_df, error_list

def convert_to_mln_format(formatted_df):
    """ convert the formatted dataframe to the MLN format 
    Example: (Tuple here is the term used in database referring to the rows in the table)
    Tuple t1 = {NAME: "ALICE JOHNSON", CITY: "DOTHAN", STATE: "AL", PHONE: "3347938701", SALARY: 50000, JOIN_DATE: "2024-01-12"}
    Tuple t2 = {NAME: "ALICE JOHNSON", CITY: "DOTH",   STATE: "AL", PHONE: "3347938701", SALARY: 50000, JOIN_DATE: "2024-01-12"}
    Tuple t3 = {NAME: "ALICE JOHNSON", CITY: "DOTHAN", STATE: "AL", PHONE: "3347938701", SALARY: 50000, JOIN_DATE: "2024-01-12"}
    returns [t1, t2, t3]
    """
    return formatted_df.to_dict(orient='records')



"""
Note:
Frontend handles:
    1. user verification for uploading the correct file to process
    2. user verification for the formatted data'
    3. user verification for the formatted data's year format: \
        - set default min and max year (so when sent to backend, both are filled 
"""