import pandas as pd

# read csv file
df = pd.read_csv('python/projects/sandbox/date_issue.csv')
# print(df.count())


# Print the initial 'Date' column to understand its content
print("Before conversion, 'Date' column:")
print(df['Date'].head(20))

# Display initial data types
print("Before Conversion:")
print(df.info())

# Step 1: Remove row 24 where Date is NaN
df = df.dropna(subset=['Date'])

# Converting 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Display data types after conversion
print("\nAfter Conversion:")
print(df.info())