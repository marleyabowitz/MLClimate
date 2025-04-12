from datetime import datetime
from meteostat import Stations, Daily
import pandas as pd

# Define time range
start = datetime(2005, 1, 1)
end   = datetime(2025, 3, 31)

# Get stations in California (bounding box)
stations = Stations()
stations = stations.bounds((42.0, -124.5), (32.0, -114.0))
stations = stations.inventory('daily', (start, end))
station_list = stations.fetch(80)  # Adjust as needed

print(f"Number of stations found: {len(station_list)}")

# Container for data
all_data = []

# Loop through stations and fetch data
for station_id, row in station_list.iterrows():
    lat = row['latitude']
    lon = row['longitude']
    print(f"Fetching data for {station_id} - {row['name']}")

    try:
        # Get daily data
        daily = Daily(station_id, start, end)
        df = daily.fetch()

        # Skip if no data
        if df.empty:
            continue

        # Ensure 'wspd' exists and has any non-null values
        if 'wspd' not in df.columns or df['wspd'].isnull().all():
            print(f"Skipping station {station_id} - No wind speed data")
            continue

        # Drop days where wspd is missing
        df = df[['wspd']].dropna(subset=['wspd'])

        # Weekly average of wind speed
        df = df.resample('W').mean()

        # Add metadata back in
        df['station_id'] = station_id
        df['lat']        = lat
        df['lon']        = lon
        df['date']       = df.index

        all_data.append(df)

    except Exception as e:
        print(f"Error with station {station_id}: {e}")

# Combine all station data
result = pd.concat(all_data)

# Remove any remaining NaNs (if a whole week was empty)
result.dropna(subset=['wspd'], inplace=True)

print("Done! Dataset shape:", result.shape)

# Save to CSV
result.to_csv('weekly_windspeed_ca_stations.csv', index=False)