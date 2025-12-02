import os
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

    # -------------------------------------------------------
    # STEP 2: ADD AUDIT COLUMN
    # -------------------------------------------------------
    @staticmethod
    def add_audit_column(df: pd.DataFrame) -> pd.DataFrame:
        df["dt_load"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        return df

    # -------------------------------------------------------
    # STEP 3: SAVE TO PARQUET (STAGE)
    # -------------------------------------------------------
    def save_stage_parquet(self, df: pd.DataFrame):
        table = pa.Table.from_pandas(df, preserve_index=False)
        pq.write_table(table, self.stage_parquet_path)

    # -------------------------------------------------------
    # STEP 4: LOAD INTO DUCKDB
    # -------------------------------------------------------
    def load_into_duckdb(self, table_name="fact_data"):
        con = duckdb.connect(self.duckdb_path)
        con.execute(f"""
            CREATE OR REPLACE TABLE {table_name} AS
            SELECT *
            FROM parquet_scan('{self.stage_parquet_path}');
        """)
        return con, table_name

    # -------------------------------------------------------
    # STEP 5: WRITE PARTITIONED PARQUET
    # -------------------------------------------------------
    def write_partitioned_parquet(self, con, table_name, partition_by="dt_load"):
        """
        Writes DuckDB table to partitioned parquet output_dir/partition=value/*.parquet
        """
        con.execute(f"""
            COPY (SELECT * FROM {table_name})
            TO '{self.output_dir}'
            (FORMAT PARQUET, PARTITION_BY ({partition_by}));
        """)

    # -------------------------------------------------------
    # RUN THE FULL PIPELINE
    # -------------------------------------------------------
    def run(self):
        print("Reading and cleaning CSV...")
        df = self.read_and_clean_csv()

        print("Adding audit column...")
        df = self.add_audit_column(df)

        print("Saving stage parquet...")
        self.save_stage_parquet(df)

        print("Loading into DuckDB...")
        con, table_name = self.load_into_duckdb()

        print("Writing partitioned parquet output...")
        self.write_partitioned_parquet(con, table_name)

        print("Pipeline finished ✔")


# =====================================================================
# Example Usage
# =====================================================================
if __name__ == "__main__":
    schema_definition = {
        "id": "int",
        "name": "string",
        "age": "float",
        "country": "string",
        "purchase_amount": "float",
        "tax": "float"
    }

    pipeline = DataPipeline(
        csv_path="input_data.csv",
        duckdb_path="example.duckdb",
        stage_parquet_path="stage_data.parquet",
        output_dir="final_parquet_output",
        schema=schema_definition
    )

    pipeline.run()
