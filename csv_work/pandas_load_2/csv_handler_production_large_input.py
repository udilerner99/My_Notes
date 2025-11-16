import pandas as pd
import logging
import os
from datetime import datetime
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LargeFileProcessor:
    """
    A class to handle large file processing tasks such as capping values, separating bad records,
    and saving data in the desired format.
    """

    def __init__(self, input_file, output_format, chunksize=100000):
        """
        Initialize the LargeFileProcessor with input file, output format, and chunk size.

        Args:
            input_file (str): Path to the input CSV file.
            output_format (str): Desired output format ('csv' or 'parquet').
            chunksize (int): Number of rows to process per chunk.
        """
        self.input_file = input_file
        self.output_format = output_format
        self.chunksize = chunksize
        self.current_folder = os.getcwd()
        self.output_clean = os.path.join(self.current_folder, f'output_cleaned.{self.output_format}')
        self.output_bad = os.path.join(self.current_folder, f'output_issues.{self.output_format}')
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Initialize output files
        if self.output_format == 'csv':
            # Write headers to the output files
            pd.DataFrame().to_csv(self.output_clean, index=False)
            pd.DataFrame().to_csv(self.output_bad, index=False)
        elif self.output_format == 'parquet':
            # Parquet does not require headers to be written first
            pass

    def process_chunk(self, chunk):
        """
        Process a single chunk of data:
        - Validate 'Date' column
        - Collect rows with NaN values
        - Cap 'Duration' values
        - Separate cleaned and bad records
        """
        try:
            # Validate 'Date' column
            chunk['Date'] = pd.to_datetime(chunk['Date'], errors='coerce')
            invalid_date_rows = chunk[chunk['Date'].isna()].copy()  # Explicitly create a copy
            chunk = chunk[chunk['Date'].notna()]

            # Collect rows with NaN values
            nan_rows = chunk[chunk.isnull().any(axis=1)].copy()  # Explicitly create a copy
            chunk = chunk.dropna()

            # Cap 'Duration' values at 120
            duration_above_120 = chunk[chunk['Duration'] > 120].copy()  # Explicitly create a copy
            chunk.loc[:, 'Duration'] = chunk['Duration'].clip(upper=120)

            # Add audit timestamp
            invalid_date_rows['dt_audit'] = self.timestamp
            nan_rows['dt_audit'] = self.timestamp
            duration_above_120['dt_audit'] = self.timestamp
            chunk['dt_audit'] = self.timestamp

            # Combine all bad records
            bad_records = pd.concat([invalid_date_rows, nan_rows, duration_above_120])

            return chunk, bad_records
        except Exception as e:
            logging.error(f"Error processing chunk: {e}")
            raise

    def save_chunk(self, df, file_path):
        """
        Save a chunk of data to the specified file.

        Args:
            df (pd.DataFrame): The DataFrame to save.
            file_path (str): The path to save the file.
        """
        try:
            if self.output_format == 'csv':
                df.to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False)
            elif self.output_format == 'parquet':
                df.to_parquet(file_path, engine='pyarrow', index=False, append=True)
        except Exception as e:
            logging.error(f"Error saving chunk to {file_path}: {e}")
            raise

    def process(self):
        """
        Process the input file in chunks and save the cleaned and bad records.
        """
        try:
            for chunk in pd.read_csv(self.input_file, chunksize=self.chunksize):
                logging.info(f"Processing a chunk of size {len(chunk)}...")
                cleaned_chunk, bad_chunk = self.process_chunk(chunk)
                self.save_chunk(cleaned_chunk, self.output_clean)
                self.save_chunk(bad_chunk, self.output_bad)
        except Exception as e:
            logging.error(f"An error occurred during processing: {e}")
            raise


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Process a large CSV file.")
    parser.add_argument('--output_format', default='csv', choices=['csv', 'parquet'], help="Output file format (csv or parquet). Defaults to 'csv'.")
    args = parser.parse_args()

    # Define input file path
    current_folder = os.getcwd()
    input_file = os.path.join(current_folder, 'data_dirty.csv')

    # Initialize and run the LargeFileProcessor
    processor = LargeFileProcessor(input_file, args.output_format)
    processor.process()

if __name__ == "__main__":
    main()