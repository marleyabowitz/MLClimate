# graphStations.py

import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the weekly CSV (output of tempData.py)
df = pd.read_csv('weekly_winddir_ca_stations.csv')

# 2. Extract unique station locations
stations = df[['station_id', 'lat', 'lon']].drop_duplicates()

# 3. Plot
plt.figure(figsize=(8, 8))
plt.scatter(stations['lon'], stations['lat'], s=20)  # one point per station

# 4. Zoom to California bbox
plt.xlim(-124.5, -114.0)
plt.ylim(32.0, 42.0)

# 5. Labels and title
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Weather Station Locations in California')

plt.tight_layout()
plt.show()