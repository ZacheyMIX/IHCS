import re
import pandas as pd
import numpy as np
import os

# Function to standardize EmployeeID format to match the pattern in Cleaned-Data.csv
def standardize_employee_id(employee_id):
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', str(employee_id))

    # Check if we have enough digits to format
    if len(digits_only) >= 10:
        # If the ID doesn't start with 0, add it
        if not digits_only.startswith('0'):
            digits_only = '0' + digits_only

        # Format as XXXX-XXX-XXX or XXXX-XXX-XXXX depending on length
        return f"{digits_only[:4]}-{digits_only[4:7]}-{digits_only[7:11]}"
    else:
        # If not enough digits, pad with zeros at the beginning
        padded_digits = digits_only.zfill(10)
        return f"{padded_digits[:4]}-{padded_digits[4:7]}-{padded_digits[7:]}"

def remove_missing_rows_all_columns(missing_rows_df, df_res):
    """ Identify duplicated rows in the ground truth dataframe that has been cleaned and might not be cleaned in the system result and removed them in the system result for preparation before evaluation """

    # Reset the index of df_res to create a column with the original indices
    df_res_with_index = df_res.reset_index().rename(columns={'index': 'original_index'})

    # Perform the merge, which will keep the original_index column
    matching_rows = pd.merge(
        df_res_with_index,
        missing_rows_df,
        on=['First Name', 'Middle Name', 'Last Name', 'Title', 'EmployeeID', 'Year of Service'],
        how='inner'
    )

    # Now matching_rows contains the original_index column with the indices from df_res
    original_indices = matching_rows['original_index'].tolist()

    print(f"The matching rows in df_res have indices: {original_indices}")

    # remove the matching rows in df_res
    df_res.drop(original_indices, inplace=True)

    return df_res

def identify_modified_columns(original_df, cleaned_df):
    """
    Identify columns that were modified during cleaning

    Args:
        original_df: The original messy dataframe
        cleaned_df: The cleaned dataframe

    Returns:
        List of column names that were modified
    """
    modified_columns = []

    # Ensure both dataframes have the same index for comparison
    original_df = original_df.reset_index(drop=True)
    cleaned_df = cleaned_df.reset_index(drop=True)

    # Check each column for differences
    for col in original_df.columns:
        if col in cleaned_df.columns:
            # Check if the column values are different
            if not original_df[col].equals(cleaned_df[col]):
                modified_columns.append(col)

    return modified_columns

def convert_to_float(weight):
    weight = weight.split(' ')[0]
    w = float(weight)
    weight = str(w) + ' lbs'
    return weight

def data_prep_ihcs(ihcs_res, gt, missing_rows_df):
    # make a copy to keep the original
    ihcs_res_copy = ihcs_res.copy()
    gt_copy = gt.copy()

    # Apply the standardization to the EmployeeID column and Weight
    ihcs_res_copy['EmployeeID'] = ihcs_res_copy['EmployeeID'].apply(standardize_employee_id)
    gt_copy['Weight'] = gt_copy['Weight'].apply(convert_to_float)

    # sort the ground truth dataframe by first name following the ihcs result
    gt_fname_sorted = gt_copy.sort_values(by = 'First Name')

    # remove duplicated rows
    ihcs_result_no_dup = remove_missing_rows_all_columns(missing_rows_df, ihcs_res_copy)

    return gt_fname_sorted, ihcs_result_no_dup

def evaluate_column_with_duplicates(df, gt, col):
    # Make copies to avoid modifying the original dataframes
    df = df.copy().reset_index()
    gt = gt.copy().reset_index()

    # Merge dataframes on EmployeeID to align rows
    merged = pd.merge(gt[['EmployeeID', col]],
                     df[['EmployeeID', col]],
                     on='EmployeeID',
                     how='left',
                     suffixes=('_gt', '_cleaned'))

    # Compute correctness
    merged['correct'] = (merged[f'{col}_gt'] == merged[f'{col}_cleaned']).astype(int)

    # Create mismatch dataframe
    mismatches = merged[merged['correct'] == 0]
    mismatch_df = pd.DataFrame({
        'EmployeeID': mismatches['EmployeeID'],
        'Cleaned': mismatches[f'{col}_cleaned'],
        'Solution': mismatches[f'{col}_gt']
    })

    return merged['correct'].values, mismatch_df

def evaluate_column_with_metrics(df, gt, col):
    """
    Evaluates a column in the cleaned dataframe against the ground truth with detailed metrics.

    Args:
        df: Cleaned dataframe
        gt: Ground truth dataframe
        col: Column name to evaluate

    Returns:
        metrics: Dictionary containing accuracy, precision, recall, and F1 score
        mismatch_df: DataFrame showing mismatches between cleaned and ground truth
    """
    # Make copies to avoid modifying the original dataframes
    df = df.copy().reset_index(drop=True)
    gt = gt.copy().reset_index(drop=True)

    # Merge dataframes on EmployeeID to align rows
    merged = pd.merge(gt[['EmployeeID', col]],
                     df[['EmployeeID', col]],
                     on='EmployeeID',
                     how='outer',
                     suffixes=('_gt', '_cleaned'))

    # Calculate correctness
    merged['correct'] = (merged[f'{col}_gt'] == merged[f'{col}_cleaned']).astype(int)

    # Fill NaN values for display in the mismatch dataframe
    merged[f'{col}_cleaned'] = merged[f'{col}_cleaned'].fillna('MISSING')
    merged[f'{col}_gt'] = merged[f'{col}_gt'].fillna('MISSING')

    # Create mismatch dataframe
    mismatches = merged[merged['correct'] == 0]
    mismatch_df = pd.DataFrame({
        'EmployeeID': mismatches['EmployeeID'],
        'Cleaned': mismatches[f'{col}_cleaned'],
        'Solution': mismatches[f'{col}_gt']
    })

    # Calculate metrics for data cleaning evaluation
    total_gt = len(gt)
    total_cleaned = len(df)
    total_merged = len(merged)

    # Entries present in both datasets
    common_entries = merged.dropna(subset=[f'{col}_gt', f'{col}_cleaned']).shape[0]

    # Correct entries (where cleaned matches ground truth)
    correct_entries = merged['correct'].sum()

    # Accuracy: proportion of correct entries among all entries
    accuracy = correct_entries / total_merged if total_merged > 0 else 0

    # Precision: proportion of correct entries among all entries in cleaned data
    # (How many of the cleaned values are correct?)
    precision = correct_entries / total_cleaned if total_cleaned > 0 else 0

    # Recall: proportion of ground truth entries that were correctly cleaned
    # (How many of the ground truth values did we correctly clean?)
    recall = correct_entries / total_gt if total_gt > 0 else 0

    # F1 score: harmonic mean of precision and recall
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    metrics = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1score': f1,
        'total_gt_entries': total_gt,
        'total_cleaned_entries': total_cleaned,
        'total_merged_entries': total_merged,
        'common_entries': common_entries,
        'correct_entries': correct_entries,
        'missing_in_cleaned': total_gt - common_entries,
        'extra_in_cleaned': total_cleaned - common_entries
    }

    return metrics, mismatch_df, merged['correct'].values

def evaluate_all_modified_columns(df, gt, columns_to_evaluate):
    res = {'accuracy': [], 'precision': [], 'recall': [], 'f1score': []}
    for col in columns_to_evaluate:
        metrics, _, _ = evaluate_column_with_metrics(df, gt, col)
        print(f'{col}: {metrics}')
        res['accuracy'].append(metrics['accuracy'])
        res['precision'].append(metrics['precision'])
        res['recall'].append(metrics['recall'])
        res['f1score'].append(metrics['f1score'])
        print('')

    res['accuracy'] = np.mean(res['accuracy'])
    res['precision'] = np.mean(res['precision'])
    res['recall'] = np.mean(res['recall'])
    res['f1score'] = np.mean(res['f1score'])

    return res

def data_prep_openrefine(openrefine_res, gt):
    # make a copy to keep the original
    openrefine_res_copy = openrefine_res.copy()
    gt_copy = gt.copy()

    # apply standardization to EmployeeID and datetime type columns
    openrefine_res_copy['EmployeeID'] = openrefine_res_copy['EmployeeID'].apply(standardize_employee_id)
    gt_copy['DOB'] = pd.to_datetime(gt_copy['DOB']).dt.strftime('%Y-%m-%dT00:00:00Z')
    gt_copy['JoinDate'] = pd.to_datetime(gt_copy['JoinDate']).dt.strftime('%Y-%m-%dT00:00:00Z')

    # remove the duplicate rows on openrefine res
    openrefine_res_no_dup = openrefine_res_copy.drop([2, 19], axis=0)

    return gt_copy, openrefine_res_no_dup

def main(messy_data_path, gt_data_path):
    current_dir = os.path.dirname(__file__)
    cleaned_data_path = os.path.join(current_dir, 'results', 'final_cleaned.csv')
    openrefine_data_path = os.path.join(current_dir, 'data', 'formatted_data_openrefine.csv')
    gt_w_dup_data_path = os.path.join(current_dir, 'data', 'cleaned_data_w_duplicates.csv')

    # Load the files
    messy_data = pd.read_csv(messy_data_path)
    ground_truth = pd.read_csv(gt_data_path, index_col=0)
    ihcs_result = pd.read_csv(cleaned_data_path, index_col=0)
    openrefine_result = pd.read_csv(openrefine_data_path)
    gt_w_dup = pd.read_csv(gt_w_dup_data_path, index_col=0)
    
    # gtdup.index = 2 : ihcs_res.index = 1
    # gtdup.index = 19 : ihcs_res.index = 21
    missing_rows_df = gt_w_dup.iloc[[2,19]][['First Name', 'Middle Name', 'Last Name', 'Title', 'EmployeeID', 'Year of Service']]

    gt_fname_sorted, ihcs_result_no_dup = data_prep_ihcs(ihcs_result, ground_truth, missing_rows_df)
    gt_modified, openrefine_res_no_dup = data_prep_openrefine(openrefine_result, ground_truth)

    ihcs_columns_modified = identify_modified_columns(messy_data, ihcs_result_no_dup)
    openrefine_columns_modified = identify_modified_columns(messy_data, openrefine_result)

    print("Columns modified in system result:", ihcs_columns_modified)
    print("Columns modified in openrefine result:", openrefine_columns_modified)

    # remove EmployeeID from modified columns
    ihcs_columns_modified.remove('EmployeeID')

    # evaluate each modified columns
    ihcs_res = evaluate_all_modified_columns(ihcs_result_no_dup, gt_fname_sorted, ihcs_columns_modified)
    openrefine_res = evaluate_all_modified_columns(openrefine_res_no_dup, gt_modified, openrefine_columns_modified)
    
    print(f'ihcs res: {ihcs_res}')
    print(f'openrefine res: {openrefine_res}')
    
    res_frontend = {'dirty_dataset': 'Messy-Data.csv', 'our_result_dataset': 'final_cleaned.csv', 'ihcs': ihcs_res, 'openrefine': openrefine_res}
    print(res_frontend)
