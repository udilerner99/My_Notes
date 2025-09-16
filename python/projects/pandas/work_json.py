import pandas as pd

# Load the JSON file into a DataFrame
df = pd.read_json("D:\workfiles\my_notes\My_Notes\python\projects\pandas\source.json")

# Convert the 'name' column to uppercase
df['name'] = df['name'].str.upper()

# Change Alice's department to 'Finance'
df.loc[df['name'] == 'ALICE', 'department'] = 'Finance'

# Add a new column 'indication' based on whether the department is 'Finance'
df['indication'] = df['department'].apply(lambda x: 'Y' if x == 'Finance' else 'N')

# Calculate the average of the 'age' column and add it as a new column 'average_age'
average_age = df['age'].mean()
df['average_age'] = average_age

# Add a new column 'age_indication' based on whether the age is above the average
df['age_indication'] = df['age'].apply(lambda x: 'Y' if x > average_age else 'N')

# Print the modified DataFrame
print(df)

# Print the number of names (i.e., the number of rows in the DataFrame)
print(f"Number of names: {len(df)}")

# Save the modified DataFrame back to the JSON file
df.to_json("D:\workfiles\my_notes\My_Notes\python\projects\pandas\source.json", orient='records', lines=False, indent=4)

#    id     name  age   department indication  average_age age_indication
# 0   1    ALICE   28      Finance          Y         29.0              N
# 1   2      BOB   34  Engineering          N         29.0              Y
# 2   3  CHARLIE   25    Marketing          N         29.0              N
# Number of names: 3