import pandas as pd
import os

# Load the main fire data
fire_df = pd.read_csv('fireData.csv')

# Convert week_start to datetime and extract year-month for matching
fire_df['week_start'] = pd.to_datetime(fire_df['week_start'])
fire_df['year_month'] = fire_df['week_start'].dt.strftime('%Y%m')

# Initialize new columns
fire_df['precipitation'] = None
fire_df['zindex'] = None
fire_df['pdsi'] = None

# Mapping of folder name to column name
data_types = {
    'precipitation': 'precipitation',
    'zindex': 'zindex',
    'pdsi': 'pdsi'
}

# Base path where the three folders are
base_path = 'data'

# For each data type
for folder, col_name in data_types.items():
    folder_path = os.path.join(base_path, folder)

    for file in os.listdir(folder_path):
        if file.endswith('.csv'):
            county_code = file.split('.')[0]  # ALA, YUB, etc.
            file_path = os.path.join(folder_path, file)

            # Read and clean the data
            df = pd.read_csv(file_path, comment='#')
            df = df[df['Value'] != -99]  # Remove missing indicators
            df['Date'] = df['Date'].astype(str)

            # For each month-year value in the file
            for _, row in df.iterrows():
                ym = row['Date']  # like '201401'
                val = row['Value']
                print(ym)

                # Update all matching rows in fire_df
                match = (fire_df['county'] == county_code) & (fire_df['year_month'] == ym)
                fire_df.loc[match, col_name] = val

# Drop the helper year_month column
fire_df = fire_df.drop(columns=['year_month'])

# Optionally save to a new file
fire_df.to_csv('fireData_with_climate.csv', index=False)

print("Data successfully merged and saved as fireData_with_climate.csv.")
