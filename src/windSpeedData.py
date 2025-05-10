from datetime import datetime
from meteostat import Stations, Daily
import pandas as pd

# time range (I ended up using a smaller one)
start = datetime(2005, 1, 1)
end   = datetime(2025, 3, 31)

# CA weather stations
stations = Stations()
stations = stations.bounds((42.0, -124.5), (32.0, -114.0))
stations = stations.inventory('daily', (start, end))
station_list = stations.fetch(80)  # Adjust as needed

print(f"Number of stations found: {len(station_list)}")

all_data = []

for station_id, row in station_list.iterrows():
    lat = row['latitude']
    lon = row['longitude']
    print(f"Fetching data for {station_id} - {row['name']}")

    try:
        # daily data
        daily = Daily(station_id, start, end)
        df = daily.fetch()

        if df.empty:
            continue

        if 'wspd' not in df.columns or df['wspd'].isnull().all():
            print(f"Skipping station {station_id} - No wind speed data")
            continue

        # drop missing days
        df = df[['wspd']].dropna(subset=['wspd'])

        # weekly average
        df = df.resample('W').mean()

        # metadata
        df['station_id'] = station_id
        df['lat']        = lat
        df['lon']        = lon
        df['date']       = df.index

        all_data.append(df)

    except Exception as e:
        print(f"Error with station {station_id}: {e}")

result = pd.concat(all_data)

# remove NaNs 
result.dropna(subset=['wspd'], inplace=True)

print("Done! Dataset shape:", result.shape)

# save
result.to_csv('windSpeed.csv', index=False)
