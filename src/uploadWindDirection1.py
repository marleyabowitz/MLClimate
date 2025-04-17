import pandas as pd
import geopandas as gpd

# Load grid with assigned stations
grid_with_stations = gpd.read_file("final_grid_with_stations.gpkg")
grid_with_stations['week_start'] = pd.to_datetime(grid_with_stations['week_start'])

# Load wind speed data
wind_df = pd.read_csv("data/windDirection.csv", parse_dates=['date'])
wind_df['week_start'] = wind_df['date'] - pd.to_timedelta(wind_df['date'].dt.dayofweek, unit='d')

# Reduce wind_df to only necessary columns and filter out early dates
wind_df = wind_df[wind_df['week_start'] >= grid_with_stations['week_start'].min()]
wind_df = wind_df[['station_id', 'week_start', 'wdir']]

# We'll write results to this file in chunks
output_file = "grid_with_windDirection.csv"
first_chunk = True

for week in grid_with_stations['week_start'].drop_duplicates():
    grid_week = grid_with_stations[grid_with_stations['week_start'] == week]
    wind_week = wind_df[wind_df['week_start'] == week]

    merged = pd.merge(
        grid_week,
        wind_week,
        left_on=['assigned_station_id', 'week_start'],
        right_on=['station_id', 'week_start'],
        how='left'
    )

    # Keep only essential columns to minimize size
    merged = merged[['grid_id', 'week_start', 'wdir']]

    # Append to CSV in chunks
    merged.to_csv(output_file, mode='a', index=False, header=first_chunk)
    first_chunk = False

    print(f"Processed week {week.date()} with {len(merged)} rows.")