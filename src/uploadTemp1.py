import pandas as pd
import geopandas as gpd

# Load grid with assigned stations
grid_with_stations = gpd.read_file("final_grid_with_stations.gpkg")
grid_with_stations['week_start'] = pd.to_datetime(grid_with_stations['week_start'])

# Load temperature data
temp_df = pd.read_csv("data/temp.csv", parse_dates=['date'])
temp_df['week_start'] = temp_df['date'] - pd.to_timedelta(temp_df['date'].dt.dayofweek, unit='d')

# Reduce temp_df to only necessary columns and filter out early dates
temp_df = temp_df[temp_df['week_start'] >= grid_with_stations['week_start'].min()]
temp_df = temp_df[['station_id', 'week_start', 'tavg']]

# We'll write results to this file in chunks
output_file = "grid_with_temperature_chunks.csv"
first_chunk = True

for week in grid_with_stations['week_start'].drop_duplicates():
    grid_week = grid_with_stations[grid_with_stations['week_start'] == week]
    temp_week = temp_df[temp_df['week_start'] == week]

    merged = pd.merge(
        grid_week,
        temp_week,
        left_on=['assigned_station_id', 'week_start'],
        right_on=['station_id', 'week_start'],
        how='left'
    )

    # Keep only essential columns to minimize size
    merged = merged[['grid_id', 'week_start', 'tavg']]

    # Append to CSV in chunks
    merged.to_csv(output_file, mode='a', index=False, header=first_chunk)
    first_chunk = False

    print(f"Processed week {week.date()} with {len(merged)} rows.")