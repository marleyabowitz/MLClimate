from datetime import datetime
from meteostat import Stations, Daily
import pandas as pd

# Define time range
start = datetime(2013, 1, 1)
end = datetime(2025, 3, 31)

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

        if df.empty:
            continue

        # Ensure 'tavg' exists and contains data
        if 'tavg' not in df.columns or df['tavg'].isnull().all():
            if 'tmin' in df.columns and 'tmax' in df.columns:
                df['tavg'] = (df['tmin'] + df['tmax']) / 2
            else:
                print(f"Skipping station {station_id} - No valid temperature data")
                continue  # Skip station if no valid temp data

        # If 'tavg' is still missing, fill using the mean of 'tmin' and 'tmax'
        if df['tavg'].isnull().any():
            if 'tmin' in df.columns and 'tmax' in df.columns:
                df['tavg'] = (df['tmin'] + df['tmax']) / 2  # Explicit assignment to avoid inplace warning
            else:
                print(f"Skipping station {station_id} - No valid temperature data")
                continue

        # Weekly average
        df = df[['tavg']]
        df = df.resample('W').mean()

        # Add metadata
        df['station_id'] = station_id
        df['lat'] = lat
        df['lon'] = lon
        df['date'] = df.index

        all_data.append(df)

    except Exception as e:
        print(f"Error with station {station_id}: {e}")

# Combine all data
result = pd.concat(all_data)

# Remove rows with any missing tavg values after resampling
result.dropna(subset=['tavg'], inplace=True)

print("Done! Dataset shape:", result.shape)

# Save to CSV
result.to_csv('weekly_tavg_ca_stations.csv', index=False)
