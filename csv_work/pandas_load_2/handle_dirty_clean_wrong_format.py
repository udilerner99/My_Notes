import pandas as pd

df = pd.read_csv('data_dirty.csv')

# convert all cells in the 'Date' column into dates.
df['Date'] = pd.to_datetime(df['Date'], format='mixed')

print(df.info())
print(df.to_string())

# Remove rows with a NULL value in the "Date" column:
df.dropna(subset=['Date'], inplace = True)

# Create a new DataFrame with rows where 'Date' is NULL
df_null_dates = df[pd.isnull(df['Date'])]

df.to_parquet('cleaned_data.parquet')
df_null_dates.to_parquet('null_dates.parquet')