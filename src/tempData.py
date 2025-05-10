from datetime import datetime
from meteostat import Stations, Daily
import pandas as pd

# time range (I ended up using a smaller range)
start = datetime(2013, 1, 1)
end = datetime(2025, 3, 31)

# stations in CA
stations = Stations()
stations = stations.bounds((42.0, -124.5), (32.0, -114.0))
stations = stations.inventory('daily', (start, end))
station_list = stations.fetch(80) 

print(f"Number of stations found: {len(station_list)}")

all_data = []

for station_id, row in station_list.iterrows():
    lat = row['latitude']
    lon = row['longitude']
    print(f"Fetching data for {station_id} - {row['name']}")

    try:
        daily = Daily(station_id, start, end)
        df = daily.fetch()

        if df.empty:
            continue

        if 'tavg' not in df.columns or df['tavg'].isnull().all():
            if 'tmin' in df.columns and 'tmax' in df.columns:
                df['tavg'] = (df['tmin'] + df['tmax']) / 2
            else:
                print(f"Skipping station {station_id} - No valid temperature data")
                continue  # skip if no valid data

       # missing data
        if df['tavg'].isnull().any():
            if 'tmin' in df.columns and 'tmax' in df.columns:
                df['tavg'] = (df['tmin'] + df['tmax']) / 2  # Explicit assignment to avoid inplace warning
            else:
                print(f"Skipping station {station_id} - No valid temperature data")
                continue

        # creating weekly average
        df = df[['tavg']]
        df = df.resample('W').mean()

        # metadata
        df['station_id'] = station_id
        df['lat'] = lat
        df['lon'] = lon
        df['date'] = df.index

        all_data.append(df)

    except Exception as e:
        print(f"Error with station {station_id}: {e}")

# combine all
result = pd.concat(all_data)

# remove missing rows
result.dropna(subset=['tavg'], inplace=True)

print("Done! Dataset shape:", result.shape)

# save
result.to_csv('temp.csv', index=False)
