#!/usr/bin/env python3
"""
Simple Machine Data Processing Script
Reads csv files in source folder with DuckDB and saves as Parquet (no pandas dependency)
"""

import duckdb
import os
from pathlib import Path

def main():
    # Initialize DuckDB connection
    conn = duckdb.connect()
    
    # Define paths
    base_path = Path(__file__).parent.parent
    raw_source_path = base_path / "rzr_raw_source"
    output_path = base_path / "rzr_raw"
    
    # Create output directory if it doesn't exist
    output_path.mkdir(exist_ok=True)
    
    print("Starting data ingestion process...")
    
    # 1. Load machines data
    machines_path = raw_source_path / "machines" / "*.csv"
    print(f"Loading machines data from: {machines_path}")
    
    conn.execute(f"""
        CREATE TABLE machines AS 
        SELECT * FROM read_csv_auto('{machines_path}')
    """)
    
    # Save machines table as parquet
    machines_output = output_path / "machines.parquet"
    conn.execute(f"COPY machines TO '{machines_output}' (FORMAT PARQUET)")
    print(f"Machines table saved to: {machines_output}")
    
    # 2. Load sensors data
    sensors_path = raw_source_path / "sensors" / "*.csv"
    print(f"Loading sensors data from: {sensors_path}")
    
    conn.execute(f"""
        CREATE TABLE sensors AS 
        SELECT * FROM read_csv_auto('{sensors_path}')
    """)
    
    # Save sensors table as parquet
    sensors_output = output_path / "sensors.parquet"
    conn.execute(f"COPY sensors TO '{sensors_output}' (FORMAT PARQUET)")
    print(f"Sensors table saved to: {sensors_output}")
    
    # 3. Load sensor_reads data (multiple CSV files)
    sensor_reads_path = raw_source_path / "sensor_reads" / "*.csv"
    print(f"Loading sensor_reads data from: {sensor_reads_path}")
    
    # Use explicit column types to handle mixed data types (numbers and 'ERR')
    conn.execute(f"""
        CREATE TABLE sensor_reads AS 
        SELECT * FROM read_csv(
            '{sensor_reads_path}',
            header=true,
            columns={{'SensorId': 'VARCHAR', 'Timestamp': 'TIMESTAMP', 'Value': 'VARCHAR'}}
        )
    """)
    
    # Save sensor_reads table as parquet
    sensor_reads_output = output_path / "sensor_reads.parquet"
    conn.execute(f"COPY sensor_reads TO '{sensor_reads_output}' (FORMAT PARQUET)")
    print(f"Sensor_reads table saved to: {sensor_reads_output}")
    
    # Display table information
    print("\n=== Data Summary ===")
    
    # Get row counts
    machines_count = conn.execute("SELECT COUNT(*) FROM machines").fetchone()[0]
    sensors_count = conn.execute("SELECT COUNT(*) FROM sensors").fetchone()[0]
    sensor_reads_count = conn.execute("SELECT COUNT(*) FROM sensor_reads").fetchone()[0]
    
    print(f"Machines: {machines_count} rows")
    print(f"Sensors: {sensors_count} rows")
    print(f"Sensor Reads: {sensor_reads_count} rows")
    
    # Display schema information
    print("\n=== Table Schemas ===")
    print("\nMachines table:")
    machines_schema = conn.execute("DESCRIBE machines").fetchall()
    for col in machines_schema:
        print(f"  {col[0]}: {col[1]}")
    
    print("\nSensors table:")
    sensors_schema = conn.execute("DESCRIBE sensors").fetchall()
    for col in sensors_schema:
        print(f"  {col[0]}: {col[1]}")
    
    print("\nSensor_reads table:")
    sensor_reads_schema = conn.execute("DESCRIBE sensor_reads").fetchall()
    for col in sensor_reads_schema:
        print(f"  {col[0]}: {col[1]}")
    
    # Close connection
    conn.close()
    print("\nData ingestion completed successfully!")

if __name__ == "__main__":
    main()

