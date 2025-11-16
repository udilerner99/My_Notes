import pandas as pd
import logging
import os
from datetime import datetime
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataProcessor:
    """
    A class to handle data processing tasks such as capping values, separating bad records,
    and saving data in the desired format.
    """

    def __init__(self, input_file, output_format):
        """
        Initialize the DataProcessor with input file and output format.

        Args:
            input_file (str): Path to the input CSV file.
            output_format (str): Desired output format ('csv' or 'parquet').
        """
        self.input_file = input_file
        self.output_format = output_format
        self.df = None
        self.df_bad = pd.DataFrame()  # Initialize an empty DataFrame for bad records
        self.current_folder = os.getcwd()
        self.output_clean = os.path.join(self.current_folder, f'output_cleaned.{self.output_format}')
        self.output_bad = os.path.join(self.current_folder, f'output_issues.{self.output_format}')
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def load_data(self):
        """Load data from the input CSV file."""
        try:
            self.df = pd.read_csv(self.input_file)
            logging.info(f"Loaded data from {self.input_file}.")
        except FileNotFoundError:
            logging.error(f"File not found: {self.input_file}")
            raise
        except Exception as e:
            logging.error(f"Error loading data: {e}")
            raise

    def validate_date_column(self):
        """
        Validate the 'Date' column:
        - Convert the 'Date' column to datetime, allowing flexible formats.
        - Collect rows with invalid dates (NaT) into the bad records DataFrame.
        """
        try:
            logging.info("Validating 'Date' column...")
            # Attempt to convert the 'Date' column to datetime with flexible parsing
            self.df['Date'] = pd.to_datetime(self.df['Date'], errors='coerce')

            # Identify rows where 'Date' is NaT (invalid dates)
            invalid_date_rows = self.df[self.df['Date'].isna()]
            logging.info(f"Found {len(invalid_date_rows)} rows with invalid dates.")
            invalid_date_rows['dt_audit'] = self.timestamp  # Add audit timestamp to bad records
            self.df_bad = pd.concat([self.df_bad, invalid_date_rows])

            # Keep only rows with valid dates
            self.df = self.df[self.df['Date'].notna()]
            logging.info(f"Remaining rows after date validation: {len(self.df)}")
        except KeyError:
            logging.error("The 'Date' column is missing in the data.")
            raise
        except Exception as e:
            logging.error(f"Error validating 'Date' column: {e}")
            raise

    def cap_duration(self):
        """Cap 'Duration' values at 120."""
        try:
            # Identify rows with 'Duration' > 120
            duration_above_120 = self.df[self.df['Duration'] > 120]
            duration_above_120['dt_audit'] = self.timestamp  # Add audit timestamp to bad records
            self.df_bad = pd.concat([self.df_bad, duration_above_120])

            # Cap 'Duration' at 120 for the remaining rows
            self.df['Duration'] = self.df['Duration'].clip(upper=120)
            logging.info("Capped 'Duration' values at 120 and collected rows with 'Duration' > 120.")
        except KeyError:
            logging.error("The 'Duration' column is missing in the data.")
            raise
        except Exception as e:
            logging.error(f"Error capping 'Duration': {e}")
            raise

    def collect_nan_rows(self):
        """
        Collect rows with NaN values in any column into the bad records DataFrame.
        """
        try:
            nan_rows = self.df[self.df.isnull().any(axis=1)]
            nan_rows['dt_audit'] = self.timestamp  # Add audit timestamp to bad records
            self.df_bad = pd.concat([self.df_bad, nan_rows])

            # Remove rows with NaN values from the main DataFrame
            self.df = self.df.dropna()
            logging.info("Collected rows with NaN values in any column.")
        except Exception as e:
            logging.error(f"Error collecting rows with NaN values: {e}")
            raise

    def add_audit_timestamp(self):
        """Add an audit timestamp column to the cleaned DataFrame."""
        self.df['dt_audit'] = self.timestamp
        logging.info("Added 'dt_audit' column with the current timestamp.")

    def save_data(self, df, file_path):
        """
        Save a DataFrame to a file in the specified format.

        Args:
            df (pd.DataFrame): The DataFrame to save.
            file_path (str): The path to save the file.
        """
        try:
            if self.output_format == 'csv':
                df.to_csv(file_path, index=False)
            elif self.output_format == 'parquet':
                df.to_parquet(file_path, index=False)
            else:
                raise ValueError("Unsupported file format. Use 'csv' or 'parquet'.")
            logging.info(f"Saved data to {file_path} in {self.output_format} format.")
        except Exception as e:
            logging.error(f"Error saving data to {file_path}: {e}")
            raise

    def process(self):
        """
        Execute the full data processing pipeline:
        - Load data
        - Validate 'Date' column
        - Collect rows with NaN values
        - Cap 'Duration' values
        - Save cleaned and bad data
        """
        try:
            self.load_data()
            self.validate_date_column()
            self.collect_nan_rows()
            self.cap_duration()
            self.add_audit_timestamp()
            self.save_data(self.df, self.output_clean)
            self.save_data(self.df_bad, self.output_bad)
        except Exception as e:
            logging.error(f"An error occurred during processing: {e}")
            raise


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Process a CSV file.")
    parser.add_argument('--output_format', default='csv', choices=['csv', 'parquet'], help="Output file format (csv or parquet). Defaults to 'csv'.")
    args = parser.parse_args()

    # Define input file path
    current_folder = os.getcwd()
    input_file = os.path.join(current_folder, 'data_dirty.csv')

    # Initialize and run the DataProcessor
    processor = DataProcessor(input_file, args.output_format)
    processor.process()

if __name__ == "__main__":
    main()