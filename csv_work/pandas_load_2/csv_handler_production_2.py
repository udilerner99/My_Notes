import pandas as pd
import logging
import os
from datetime import datetime
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(file_path):
    """Load data from a CSV file."""
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Loaded data from {file_path}.")
        return df
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        raise

def cap_duration(df):
    """Cap 'Duration' values at 120."""
    df['Duration'] = df['Duration'].clip(upper=120)
    return df

def separate_bad_records(df):
    """Separate rows with 'Duration' > 120 into a new DataFrame."""
    df_bad = df[df['Duration'] > 120]
    df_clean = df[df['Duration'] <= 120]
    return df_clean, df_bad

def save_data(df, file_path, file_format):
    """
    Save DataFrame to a file in the specified format (CSV or Parquet).
    
    Args:
        df (pd.DataFrame): The DataFrame to save.
        file_path (str): The path to save the file.
        file_format (str): The format to save the file ('csv' or 'parquet').
    """
    try:
        if file_format == 'csv':
            df.to_csv(file_path, index=False)
        elif file_format == 'parquet':
            df.to_parquet(file_path, index=False)
        else:
            raise ValueError("Unsupported file format. Use 'csv' or 'parquet'.")
        logging.info(f"Saved data to {file_path} in {file_format} format.")
    except Exception as e:
        logging.error(f"Error saving data: {e}")
        raise

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Process a CSV file.")
    parser.add_argument('--output_format', required=True, choices=['csv', 'parquet'], help="Output file format (csv or parquet).")
    args = parser.parse_args()

    # Define dynamic paths based on the current folder
    current_folder = os.getcwd()
    input_file = os.path.join(current_folder, 'data_dirty.csv')
    output_clean = os.path.join(current_folder, 'output_cleaned.' + args.output_format)
    output_bad = os.path.join(current_folder, 'output_issues.' + args.output_format)

    # Load data
    df = load_data(input_file)

    # Add audit timestamp
    df['dt_audit'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Cap 'Duration' and separate bad records
    df_clean, df_bad = separate_bad_records(df)

    # Save outputs
    save_data(df_clean, output_clean, args.output_format)
    save_data(df_bad, output_bad, args.output_format)

if __name__ == "__main__":
    main()