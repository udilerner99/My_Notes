import os

from pyspark.sql import SparkSession

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("machines CSV to Parquet") \
    .getOrCreate()

# Define the relative directory path
base_dir = os.path.join(os.getcwd(), "sensorial_task", "data", "source", "src_machines")

# Define input and output file paths based on the relative directory
input_path = os.path.join(base_dir, "Machines.csv")
output_path = os.path.join(base_dir, "raw_Machines.parquet")

# Read CSV file into DataFrame
df = spark.read.csv(input_path, header=True, inferSchema=True)

# Write DataFrame to Parquet
df.write.parquet(output_path)

# Stop the Spark session
spark.stop()