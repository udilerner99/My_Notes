import pandas as pd

# read file
df = pd.read_csv('python/projects/sandbox/data.csv')

# print(df.to_string())
print(df.count())

# clean the data - dropping na
# df_removed_na = df.dropna()
# print(df_removed_na.count())


# replace with mean
x = df['Calories'].mean()
df['Calories'] = df['Calories'].fillna(x)
print(df.count())
