from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import DoubleType, IntegerType, StringType, DateType

# --------------------------
# Create Spark session
# --------------------------
spark = SparkSession.builder \
    .appName("SafeCSVProcessing") \
    .getOrCreate()

# --------------------------
# Load CSV
# --------------------------
csv_path = "sample_data_dirty_showcase.csv"

df = spark.read.option("header", True).option("inferSchema", False).csv(csv_path)

# --------------------------
# Safe numeric conversion
# --------------------------
numeric_cols = ["purchase_amount", "tax", "total_cost"]
for col in numeric_cols:
    df = df.withColumn(col, F.expr(f"try_cast({col} AS DOUBLE)"))

int_cols = ["id", "age"]
for col in int_cols:
    df = df.withColumn(col, F.expr(f"try_cast({col} AS INT)"))

# # --------------------------
# # Safe date parsing
# # --------------------------
# # Handles 'YYYY-MM-DD', 'YYYY/MM/DD', 'YYYYMMDD', or invalid -> NULL
# df = df.withColumn(
#     "signup_date",
#     F.coalesce(
#         F.expr("try_to_date(signup_date, 'yyyy-MM-dd')"),
#         F.expr("try_to_date(signup_date, 'yyyy/MM/dd')"),
#         F.expr(
#             "try_to_date(substr(signup_date,1,4) || '-' || substr(signup_date,5,2) || '-' || substr(signup_date,7,2), 'yyyy-MM-dd')"
#         )
#     )
# )

# # --------------------------
# # Example computed column
# # --------------------------
# # total_cost_calc = purchase_amount * (1 + tax)
# df = df.withColumn(
#     "total_cost_calc",
#     F.when(
#         F.col("purchase_amount").isNotNull() & F.col("tax").isNotNull(),
#         F.col("purchase_amount") * (1 + F.col("tax"))
#     ).otherwise(None)
# )

# # --------------------------
# # Optional: handle NULLs
# # --------------------------
# # Replace NULLs for numeric columns
# df = df.fillna({"purchase_amount": 0, "tax": 0, "total_cost": 0, "total_cost_calc": 0, "age": 0, "id": 0})

# --------------------------
# Show results safely
# --------------------------
df.show(20, truncate=False)

# --------------------------
# Stop Spark
# --------------------------
spark.stop()
