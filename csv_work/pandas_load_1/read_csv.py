import pandas as pd

df = pd.read_csv('sample_data.csv')

# print first 10 rows
# print(df.head(10))

# print first 5 rows
# print(df.head())

# print last 5 rows
# print(df.tail())

# print info about the file
print(df.info())