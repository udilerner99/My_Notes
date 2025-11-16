import pandas as pd

df = pd.read_csv('employee_salaries.csv')

# with to_string()
# print(df.to_string())

# without to_string()
print(df)