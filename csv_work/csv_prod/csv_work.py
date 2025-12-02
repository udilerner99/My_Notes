import os
import logging
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import duckdb
from datetime import datetime
from typing import Dict, Any

class DataPipeline:
    def __init__(self,
                 csv_path: str,
                 duckdb_path: str,
                 stage_parquet_path: str,
                 output_dir: str,
                 schema: Dict[str, Any]):
        """
        :param csv_path: path to input CSV
        :param duckdb_path: path to DuckDB database file
        :param stage_parquet_path: intermediate parquet file
        :param output_dir: directory where final parquet partitions will be written
        :param schema: enforced schema dict: {"colname": dtype}
        """
        
        self.csv_path = csv_path
        self.duckdb_path = duckdb_path
        self.stage_parquet_path = stage_parquet_path
        self.output_dir = output_dir
        self.schema = schema
        os.makedirs(output_dir, exist_ok=True)
        
    # -------------------------------------------------------
    # STEP 1: READ CSV with missing and invalid data handling
    # -------------------------------------------------------
    def read_and_clean_csv(self) -> pd.DataFrame:
        try:
            df = pd.read_csv(self.csv_path)

            # Handle missing columns
            for col in self.schema:
                if col not in df.columns:
                    df[col] = None  # fill missing column

            # Enforce schema (invalid values become NA)
            for col, dtype in self.schema.items():
                try:
                    df[col] = df[col].astype(dtype)
                except Exception:
                    # Convert invalid data to NaN
                    df[col] = pd.to_numeric(df[col], errors='coerce') if dtype in ["float", "int"] else df[col]

            return df
        except Exception as e:
            logging.error(f"Error reading csv file")
            raise
    
    # -------------------------------------------------------
    # STEP 2: split full name into first name and last name
    # -------------------------------------------------------
    @staticmethod
    def split_full_name(df: pd.DataFrame) -> pd.DataFrame:
        try:
            # splitting full name into 2 columns
            df[["first_name", "last_name"]] = df["full_name"].str.split(' ', expand=True)

            return df
        except Exception as e:
            logging.error(f"Error handling full name split")
            raise

    
    # -------------------------------------------------------
    # STEP 3: convert date column
    # -------------------------------------------------------
    @staticmethod
    def handle_date(df: pd.DataFrame) -> pd.DataFrame:
        # handle date convert
        try:
            df['signup_date'] = pd.to_datetime(df['signup_date'], format='%Y%m%d')

            return df
        except Exception as e:
            logging.error(f"Error handling full name split")
            raise
        
    # -------------------------------------------------------
    # STEP 4: convert amount column to USD
    # -------------------------------------------------------
    @staticmethod
    def convert_amount(df: pd.DataFrame) -> pd.DataFrame:
        # handle date convert
        try:
            df['purchase_amount'] = df['purchase_amount'] * 3.7
            print(df.head())
            return df
        except Exception as e:
            logging.error(f"Error handling full name split")
            raise
    
    # -------------------------------------------------------
    # RUN THE FULL PIPELINE
    # -------------------------------------------------------
    def run(self):
        print("Reading and cleaning CSV...")
        df = self.read_and_clean_csv()
        
        print("Splitting Full name into First & Last name columns")
        df = self.split_full_name(df)
        
        print("casting date column")
        df = self.handle_date(df)
        
        print("converting purchase amount to USD")
        df = self.convert_amount(df)

        # print("Adding audit column...")
        # df = self.add_audit_column(df)

        # print("Saving stage parquet...")
        # self.save_stage_parquet(df)

        # print("Loading into DuckDB...")
        # con, table_name = self.load_into_duckdb()

        # print("Writing partitioned parquet output...")
        # self.write_partitioned_parquet(con, table_name)

        print("Pipeline finished ✔")

# ===============================================================
# main function call setting schema definition & calling pipeline
# ===============================================================
if __name__ == "__main__":
    schema_definition = {
        "customer_id": "int",
        "full_name": "string",
        "email": "string",
        "signup_date": "date",
        "purchase_amount": "float"
    }
    
    pipeline = DataPipeline(
        csv_path = "input_data_2.csv",
        duckdb_path="example.duckdb",
        stage_parquet_path="stage_data.parquet",
        output_dir="final_parquet_output",
        schema=schema_definition
    )

    pipeline.run()