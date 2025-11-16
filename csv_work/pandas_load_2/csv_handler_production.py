import pandas as pd
import argparse
import logging
from datetime import datetime

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

def save_data(df, file_path):
    """Save DataFrame to a CSV file."""
    try:
        df.to_csv(file_path, index=False)
        logging.info(f"Saved data to {file_path}.")
    except Exception as e:
        logging.error(f"Error saving data: {e}")
        raise

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Process a CSV file.")
    parser.add_argument('--input', required=True, help="Path to the input CSV file.")
    parser.add_argument('--output_clean', required=True, help="Path to save the cleaned data.")
    parser.add_argument('--output_bad', required=True, help="Path to save the bad data.")
    args = parser.parse_args()

    # Load data
    df = load_data(args.input)

    # Add audit timestamp
    df['dt_audit'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Cap 'Duration' and separate bad records
    df_clean, df_bad = separate_bad_records(df)

    # Save outputs
    save_data(df_clean, args.output_clean)
    save_data(df_bad, args.output_bad)

if __name__ == "__main__":
    main()