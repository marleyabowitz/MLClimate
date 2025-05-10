import pandas as pd

# Load your dataset
df = pd.read_csv("cleaned_fire_data.csv")  # or your original file

# Ensure 'week_start' is in datetime format
df['week_start'] = pd.to_datetime(df['week_start'])

# Extract the month and add it as a new column
df['month'] = df['week_start'].dt.month

# (Optional) Save the updated DataFrame
df.to_csv("dataPreScaling.csv", index=False)

# Preview
print(df[['week_start', 'month']].head())