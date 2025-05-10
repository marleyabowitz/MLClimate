import pandas as pd

# Load the fire data with climate info
fire_df = pd.read_csv('fireData_with_climate.csv')
fire_df['week_start'] = pd.to_datetime(fire_df['week_start'])
fire_df['year'] = fire_df['week_start'].dt.year

# Load and transform population data
pop_df = pd.read_csv('data/population.csv')

# Melt the population data from wide to long format
pop_long = pop_df.melt(id_vars=['County'], var_name='year', value_name='population')

# Clean up the data
pop_long['year'] = pop_long['year'].astype(int)
pop_long['population'] = pop_long['population'].str.replace(',', '').astype(int)
pop_long = pop_long.rename(columns={'County': 'county'})

# Merge with fire data
fire_df = fire_df.merge(pop_long, how='left', on=['county', 'year'])

# Drop helper year column if not needed
fire_df = fire_df.drop(columns=['year'])

# Save the result
fire_df.to_csv('fireData_with_climate_and_population.csv', index=False)

print("Population data merged successfully into fireData_with_climate_and_population.csv.")