import pandas as pd

df = pd.read_csv('data.csv')

# use to_string() to print the entire DataFrame.
print(df.to_string())

# use head() to print the first 5 rows of the DataFrame.
print(df.head())

# Print the last 5 rows of the DataFrame:
print(df.tail())

# Print information about the data:
print(df.info()) 