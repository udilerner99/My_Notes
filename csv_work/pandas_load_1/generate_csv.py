import csv, random
from datetime import datetime, timedelta

headers = ["id","name","age","country","signup_date","purchase_amount"]
countries = ["USA","UK","Germany","France","Israel","India","Japan","Canada"]
start_date = datetime(2020,1,1)

with open("sample_data.csv","w",newline="",encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(headers)
    for i in range(1,1501):
        w.writerow([
            i,
            f"User_{i}",
            random.randint(18,70),
            random.choice(countries),
            (start_date + timedelta(days=random.randint(0,1800))).strftime("%Y-%m-%d"),
            round(random.uniform(10.0,1000.0),2)
        ])

print("✅ sample_data.csv created successfully!")