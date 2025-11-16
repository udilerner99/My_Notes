import dask.dataframe as dd
import logging
import os
from datetime import datetime
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DaskFileProcessor:
    """
    A class to handle large file processing tasks using Dask, such as capping values,
    separating bad records, and saving data in the desired format.
    """

    def __init__(self, input_file, output_format):
        """
        Initialize the DaskFileProcessor with input file and output format.

        Args:
            input_file (str): Path to the input CSV file.
            output_format (str): Desired output format ('csv' or 'parquet').
        """
        self.input_file = input_file
        self.output_format = output_format
        self.current_folder = os.getcwd()
        self.output_clean = os.path.join(self.current_folder, f'output_cleaned.{self.output_format}')
        self.output_bad = os.path.join(self.current_folder, f'output_issues.{self.output_format}')
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def process(self):
        """
        Process the input file using Dask and save the cleaned and bad records.
        """
        try:
            logging.info("Reading the input file with Dask...")
            # Read the input file as a Dask DataFrame
            ddf = dd.read_csv(self.input_file, assume_missing=True)

            # Validate 'Date' column
            logging.info("Validating 'Date' column...")
            ddf['Date'] = dd.to_datetime(ddf['Date'], errors='coerce')
            invalid_date_rows = ddf[ddf['Date'].isna()]
            ddf = ddf[~ddf['Date'].isna()]  # Replace .notna() with ~isna()

            # Collect rows with NaN values
            logging.info("Collecting rows with NaN values...")
            nan_rows = ddf[ddf.isnull().any(axis=1)]
            ddf = ddf.dropna()

            # Cap 'Duration' values at 120
            logging.info("Capping 'Duration' values at 120...")
            duration_above_120 = ddf[ddf['Duration'] > 120]
            ddf['Duration'] = ddf['Duration'].clip(upper=120)

            # Add audit timestamp
            logging.info("Adding audit timestamp...")
            ddf['dt_audit'] = self.timestamp
            invalid_date_rows['dt_audit'] = self.timestamp
            nan_rows['dt_audit'] = self.timestamp
            duration_above_120['dt_audit'] = self.timestamp

            # Combine all bad records
            logging.info("Combining bad records...")
            bad_records = dd.concat([invalid_date_rows, nan_rows, duration_above_120])

            # Save cleaned data and bad records
            logging.info("Saving cleaned data and bad records...")
            self.save_data(ddf, self.output_clean)
            self.save_data(bad_records, self.output_bad)

        except Exception as e:
            logging.error(f"An error occurred during processing: {e}")
            raise

    def save_data(self, ddf, file_path):
        """
        Save a Dask DataFrame to the specified file.

        Args:
            ddf (dask.dataframe.DataFrame): The Dask DataFrame to save.
            file_path (str): The path to save the file.
        """
        try:
            if self.output_format == 'csv':
                ddf.to_csv(file_path, index=False, single_file=True)
            elif self.output_format == 'parquet':
                ddf.to_parquet(file_path, engine='pyarrow', write_index=False)
            logging.info(f"Saved data to {file_path} in {self.output_format} format.")
        except Exception as e:
            logging.error(f"Error saving data to {file_path}: {e}")
            raise


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Process a large CSV file using Dask.")
    parser.add_argument('--output_format', default='csv', choices=['csv', 'parquet'], help="Output file format (csv or parquet). Defaults to 'csv'.")
    args = parser.parse_args()

    # Define input file path
    current_folder = os.getcwd()
    input_file = os.path.join(current_folder, 'data_dirty.csv')

    # Initialize and run the DaskFileProcessor
    processor = DaskFileProcessor(input_file, args.output_format)
    processor.process()

if __name__ == "__main__":
    main()