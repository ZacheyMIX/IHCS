import pandas as pd
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

def get_dataset():
    """ function to get both the messy dataset and the cleaned dataset """
    cleaned_data_path = '/Users/novellaalvina/Documents/US/UTAH/Lessons/MS/Spring2025/CS 6964/project/IHCS/results/final_formatted_data.csv'    
    gt_data_path = '/Users/novellaalvina/Documents/US/UTAH/Lessons/MS/Spring2025/CS 6964/project/IHCS/potential_dataset/Cleaned-Data.csv'
    return cleaned_data_path, gt_data_path

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

def evaluate_cleaning(cleaned_df, gt_df, modified_columns=None):
    """
    Evaluate the cleaning results against ground truth
    
    Args:
        cleaned_df: The cleaned dataframe
        gt_df: The ground truth dataframe
        modified_columns: List of columns to evaluate (if None, evaluate all common columns)
    
    Returns:
        Dictionary with evaluation metrics for each column
    """
    results = {}
    
    # If no specific columns are provided, use all common columns
    if modified_columns is None:
        modified_columns = [col for col in cleaned_df.columns if col in gt_df.columns]
    
    # Ensure both dataframes have the same index for comparison
    cleaned_df = cleaned_df.reset_index(drop=True)
    gt_df = gt_df.reset_index(drop=True)
    
    # Overall statistics
    total_cells = 0
    correct_cells = 0
    
    for col in modified_columns:
        if col in gt_df.columns:
            # For categorical data, calculate precision, recall, f1
            if cleaned_df[col].dtype == 'object' or gt_df[col].dtype == 'object':
                # Convert to string to ensure proper comparison
                cleaned_values = cleaned_df[col].astype(str)
                gt_values = gt_df[col].astype(str)
                
                # Calculate cell-level accuracy
                accuracy = (cleaned_values == gt_values).mean()
                
                # For multi-class metrics, we need to handle each unique value as a class
                # This is a simplified approach - for more complex scenarios you might need
                # to adapt this based on your specific data
                try:
                    # Create binary indicators for each value
                    all_values = set(cleaned_values.unique()) | set(gt_values.unique())
                    
                    # Calculate metrics for each value and average them
                    prec_scores = []
                    rec_scores = []
                    f1_scores = []
                    
                    for value in all_values:
                        y_true = (gt_values == value).astype(int)
                        y_pred = (cleaned_values == value).astype(int)
                        
                        if sum(y_true) > 0 and sum(y_pred) > 0:
                            prec = precision_score(y_true, y_pred, zero_division=0)
                            rec = recall_score(y_true, y_pred, zero_division=0)
                            f1 = f1_score(y_true, y_pred, zero_division=0)
                            
                            prec_scores.append(prec)
                            rec_scores.append(rec)
                            f1_scores.append(f1)
                    
                    if prec_scores:
                        precision = np.mean(prec_scores)
                        recall = np.mean(rec_scores)
                        f1 = np.mean(f1_scores)
                    else:
                        precision = recall = f1 = 0.0
                        
                except Exception as e:
                    precision = recall = f1 = 0.0
                    print(f"Error calculating metrics for column {col}: {e}")
            
            # For numerical data, calculate RMSE and MAE
            elif pd.api.types.is_numeric_dtype(cleaned_df[col]) and pd.api.types.is_numeric_dtype(gt_df[col]):
                # Handle potential NaN values
                valid_mask = ~(cleaned_df[col].isna() | gt_df[col].isna())
                
                if valid_mask.sum() > 0:
                    cleaned_values = cleaned_df.loc[valid_mask, col]
                    gt_values = gt_df.loc[valid_mask, col]
                    
                    # Calculate accuracy as percentage of exact matches
                    accuracy = (cleaned_values == gt_values).mean()
                    
                    # Calculate RMSE and MAE
                    rmse = np.sqrt(((cleaned_values - gt_values) ** 2).mean())
                    mae = np.abs(cleaned_values - gt_values).mean()
                    
                    # For numerical data, precision/recall/f1 don't apply directly
                    precision = recall = f1 = None
                else:
                    accuracy = rmse = mae = 0
                    precision = recall = f1 = None
            
            # Update overall statistics
            col_cells = len(cleaned_df[col])
            total_cells += col_cells
            correct_cells += sum(cleaned_df[col].astype(str) == gt_df[col].astype(str))
            
            # Store results for this column
            results[col] = {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'type': 'categorical' if cleaned_df[col].dtype == 'object' else 'numerical'
            }
            
            # Add RMSE and MAE for numerical columns
            if pd.api.types.is_numeric_dtype(cleaned_df[col]) and pd.api.types.is_numeric_dtype(gt_df[col]):
                results[col]['rmse'] = rmse
                results[col]['mae'] = mae
    
    # Calculate overall accuracy
    results['overall'] = {
        'accuracy': correct_cells / total_cells if total_cells > 0 else 0,
        'modified_columns': len(modified_columns),
        'total_cells_evaluated': total_cells,
        'correct_cells': correct_cells
    }
    
    return results

def main():
    """ main function to run the script """

    # messy data and gt data
    messy_data_path, gt_data_path = get_dataset()
    
    # create dataframe from the uploaded file
    messy_df = pd.read_csv(messy_data_path)
    cleaned_df = pd.read_csv(messy_data_path)  # Replace this with your actual cleaned dataframe
    gt_df = pd.read_csv(gt_data_path)
    
    # Identify which columns were modified during cleaning
    modified_columns = identify_modified_columns(messy_df, cleaned_df)
    print(f"Modified columns: {modified_columns}")
    
    # Evaluate only the modified columns
    evaluation_results = evaluate_cleaning(cleaned_df, gt_df, modified_columns)
    
    # Print evaluation results
    print("\nEvaluation Results:")
    print("===================")
    
    for col, metrics in evaluation_results.items():
        if col != 'overall':
            print(f"\nColumn: {col} ({metrics['type']})")
            print(f"  Accuracy: {metrics['accuracy']:.4f}")
            
            if metrics['type'] == 'categorical':
                if metrics['precision'] is not None:
                    print(f"  Precision: {metrics['precision']:.4f}")
                    print(f"  Recall: {metrics['recall']:.4f}")
                    print(f"  F1 Score: {metrics['f1_score']:.4f}")
            else:
                if 'rmse' in metrics:
                    print(f"  RMSE: {metrics['rmse']:.4f}")
                    print(f"  MAE: {metrics['mae']:.4f}")
    
    # Print overall results
    print("\nOverall Results:")
    print(f"  Accuracy: {evaluation_results['overall']['accuracy']:.4f}")
    print(f"  Modified Columns: {evaluation_results['overall']['modified_columns']}")
    print(f"  Total Cells Evaluated: {evaluation_results['overall']['total_cells_evaluated']}")
    print(f"  Correct Cells: {evaluation_results['overall']['correct_cells']}")

if __name__ == "__main__":
    main()
