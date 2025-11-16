import csv
import random
from datetime import datetime, timedelta

csv_file = "sample_data_dirty_showcase.csv"

headers = ["id", "name", "age", "country", "signup_date", "purchase_amount", "tax", "total_cost"]
countries = ["USA", "UK", "Germany", "France", "Israel", "India", "Japan", "Canada"]
start_date = datetime(2020, 1, 1)
num_records = 1500

rows = []

# ---- 1. Showcase rows with explicit cases ----

# Normal row
purchase_amount = 500.0
tax = 0.10
total_cost = round(purchase_amount * tax, 2)
rows.append([1, "User_1", 30, "USA", "2021-01-15", purchase_amount, tax, total_cost])

# Empty / NaN
rows.append([2, "User_2", "", "NaN", "", 200.0, 0.05, "NaN"])

# Wrong format numeric
rows.append([3, "User_3", "N/A", "UK", "20220315", "error", "?", "error"])

# Wrong format date
rows.append([4, "User_4", 45, "Germany", "20250123", 300.0, 0.08, 24.0])

# Wrong data numeric
rows.append([5, "User_5", 150, "France", "2022-05-01", -500.0, 5.0, -2500.0])

# Duplicate of normal row
rows.append(rows[0].copy())

# Another row normal
rows.append([7, "User_7", 28, "India", "2020-06-10", 123.45, 0.07, round(123.45*0.07,2)])

# ---- 2. Generate remaining random rows with ~15% dirty data ----
for i in range(8, num_records + 1):
    purchase_amount = round(random.uniform(10.0, 1000.0), 2)
    tax = round(random.uniform(0.04, 0.18), 2)
    total_cost = round(purchase_amount * tax, 2)

    row = [
        i,
        f"User_{i}",
        random.randint(18, 70),
        random.choice(countries),
        (start_date + timedelta(days=random.randint(0, 1800))).strftime("%Y-%m-%d"),
        purchase_amount,
        tax,
        total_cost
    ]

    # 15% chance for dirty data
    if random.random() < 0.15:
        error_type = random.choice(["empty", "wrong_format", "wrong_data", "duplicate"])

        if error_type == "empty":
            idx = random.randint(1, len(row) - 1)
            row[idx] = random.choice(["", "NaN"])

        elif error_type == "wrong_format":
            idx = random.choice([2, 4, 5, 6, 7])  # age, signup_date, purchase_amount, tax, total_cost
            if idx == 4:  # signup_date
                row[idx] = random.choice([
                    (start_date + timedelta(days=random.randint(0, 1800))).strftime("%Y%m%d"),
                    "NaN"
                ])
            else:
                row[idx] = random.choice(["N/A", "undefined", "?", "error"])

        elif error_type == "wrong_data":
            bad_values = {
                2: [-5, 150, 999],
                5: [-50.5, 20000],
                6: [0.5, 1.0, 5.0],
                7: [-100, 20000]
            }
            idx = random.choice([2, 5, 6, 7])
            row[idx] = random.choice(bad_values[idx])

        elif error_type == "duplicate" and rows:
            row = random.choice(rows).copy()

    # Recalculate total_cost if numeric
    try:
        row[7] = round(float(row[5]) * float(row[6]), 2)
    except (ValueError, TypeError):
        pass

    rows.append(row)

# Write CSV
with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)

print(f"✅ Created '{csv_file}' with {num_records} rows, including all showcase dirty data cases.")
