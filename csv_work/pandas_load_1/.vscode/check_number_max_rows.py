# import pandas as pd

# print(pd.options.display.max_rows) 

import pandas as pd

# increase max rows
pd.options.display.max_rows = 9999

df = pd.read_csv('employee_salaries.csv')

print(df) 