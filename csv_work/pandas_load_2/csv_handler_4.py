import pandas as pd
import duckdb
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CSVToDuckDB:
    """
    A class to handle the process of reading a CSV file, converting it to Parquet,
    and loading it into a DuckDB table.
    """

    def __init__(self, csv_file, parquet_file, db_file, table_name):
        """
        Initialize the CSVToDuckDB class.

        Args:
            csv_file (str): Path to the input CSV file.
            parquet_file (str): Path to the output Parquet file.
            db_file (str): Path to the DuckDB database file.
            table_name (str): Name of the DuckDB table.
        """
        self.csv_file = csv_file
        self.parquet_file = parquet_file
        self.db_file = db_file
        self.table_name = table_name

    def read_csv(self):
        """
        Read the CSV file and parse columns with the correct types.

        Returns:
            pd.DataFrame: The parsed DataFrame.
        """
        try:
            logging.info(f"Reading CSV file: {self.csv_file}")
            # Read the CSV file
            df = pd.read_csv(self.csv_file)

            # Parse columns with correct types
            df['Duration'] = pd.to_numeric(df['Duration'], errors='coerce')
            df['Pulse'] = pd.to_numeric(df['Pulse'], errors='coerce')
            df['Maxpulse'] = pd.to_numeric(df['Maxpulse'], errors='coerce')
            df['Calories'] = pd.to_numeric(df['Calories'], errors='coerce')

            logging.info("Successfully parsed columns with correct types.")
            return df
        except Exception as e:
            logging.error(f"Error reading or parsing CSV file: {e}")
            raise

    def write_parquet(self, df):
        """
        Write the DataFrame to a Parquet file.

        Args:
            df (pd.DataFrame): The DataFrame to write.
        """
        try:
            logging.info(f"Writing DataFrame to Parquet file: {self.parquet_file}")
            df.to_parquet(self.parquet_file, index=False)
            logging.info("Successfully wrote Parquet file.")
        except Exception as e:
            logging.error(f"Error writing Parquet file: {e}")
            raise

    def load_to_duckdb(self):
        """
        Load the Parquet file into a DuckDB table. If the table does not exist, create it.
        """
        try:
            logging.info(f"Connecting to DuckDB database: {self.db_file}")
            conn = duckdb.connect(self.db_file)

            # Create the table if it doesn't exist and load the Parquet file
            logging.info(f"Loading Parquet file into DuckDB table: {self.table_name}")
            conn.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} AS
                SELECT * FROM read_parquet('{self.parquet_file}')
            """)
            logging.info(f"Successfully loaded data into DuckDB table: {self.table_name}")

            conn.close()
        except Exception as e:
            logging.error(f"Error loading data into DuckDB: {e}")
            raise

    def process(self):
        """
        Execute the full process: read CSV, write Parquet, and load into DuckDB.
        """
        try:
            # Step 1: Read the CSV file
            df = self.read_csv()

            # Step 2: Write the DataFrame to a Parquet file
            self.write_parquet(df)

            # Step 3: Load the Parquet file into DuckDB
            self.load_to_duckdb()

            logging.info("Process completed successfully.")
        except Exception as e:
            logging.error(f"An error occurred during processing: {e}")
            raise


def main():
    # Define file paths and table name
    csv_file = 'data.csv'  # Path to the input CSV file
    parquet_file = 'data.parquet'  # Path to the output Parquet file
    db_file = 'data_processing.db'  # Path to the DuckDB database file
    table_name = 'raw_data'  # Name of the DuckDB table

    # Initialize the CSVToDuckDB class and run the process
    processor = CSVToDuckDB(csv_file, parquet_file, db_file, table_name)
    processor.process()


if __name__ == "__main__":
    main()