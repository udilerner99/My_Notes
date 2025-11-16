import pandas as pd

df = pd.read_csv('data_dirty.csv')

for x in df.index:
    if df.loc[x, "Duration"] > 120:
        df.loc[x, "Duration"] = 120
        
# Vectorized operation to cap "Duration" values at 120
df['Duration'] = df['Duration'].clip(upper=120)

# Create a new DataFrame with rows where "Duration" > 120
df_duration_above_120 = df[df['Duration'] > 120]

# Remove rows with "Duration" > 120 from the original DataFrame
df = df[df['Duration'] <= 120]

# Save the new DataFrame if needed
df_duration_above_120.to_csv('duration_above_120.csv', index=False)