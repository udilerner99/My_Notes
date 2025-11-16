# tax column:
# Normal values: 0.04 – 0.18
# Wrong data: 0.5, 1.0, 5.0 (simulate unrealistic taxes)
# signup_date wrong formats: YYYYMMDD or "NaN"
# total_cost recalculated if numeric
# 15% of rows randomly get errors:
# Empty / "NaN"
# Wrong formats (N/A, ?, error)
# Wrong data (including high tax)
# Duplicates

import pandas as pd

# read the csv
df = pd.read_csv('sample_data_dirty_showcase.csv')

# new dataframe with no na
# df_dropna = df.dropna()

# output 10 rows from head
print(df.head(10))

# instead of drop rows - replace with a specific value - will handle depend on column
df.fillna({"id": -1}, inplace=True)
df.fillna({"name": "na"}, inplace=True)
df.fillna({"age": -1}, inplace=True)
df.fillna({"country": "na"}, inplace=True)

# clean format issue
df['signup_date'] = pd.to_datetime(df['signup_date'], format='mixed')

# convert measures into int / decimal
df['purchase_amount'] = pd.to_numeric(df['purchase_amount'], errors='coerce')
df['tax'] = pd.to_numeric(df['tax'], errors='coerce')
df['total_cost'] = pd.to_numeric(df['total_cost'], errors='coerce')


# Remove rows with a NULL value in the "Date" column:
# df.dropna(subset=['signup_date'], inplace = True)

# instead of drop rows - replace with na date
df.fillna({"signup_date": "1900-01-01"}, inplace=True)

# fix max value of purchase_amount max should be 900
# vercorized
df.loc[df['purchase_amount'] > 900, 'purchase_amount'] = 900

# clip
df['purchase_amount'] = df['purchase_amount'].clip(upper=900)

# Fill missing total_cost with purchase_amount * tax
df.loc[df['total_cost'].isna(), 'total_cost'] = (
    df['purchase_amount'] * df['tax']
)

# check for duplicate rows
# print(df.duplicated())

df.drop_duplicates(inplace = True)

# output df info
print(df.info())

# output 10 rows from head
print(df.head(10))