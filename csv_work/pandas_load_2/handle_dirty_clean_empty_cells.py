import pandas as pd

df = pd.read_csv('data_dirty.csv')

print(df.info())

new_df = df.dropna()

print(new_df.info())
print(new_df.to_string())

# remove rows with any missing values in place
df.dropna(inplace=True)

# replace empty cells with a specific value
df.fillna({"Calories": 130}, inplace=True)