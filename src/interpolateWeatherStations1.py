import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree

# Load the final grid
final_grid = gpd.read_file("final_grid.gpkg")

# Get unique grid cells (drop duplicates from time dimension)
unique_grid = final_grid[['grid_id', 'geometry']].drop_duplicates().copy()

# Calculate centroids of grid cells
unique_grid['centroid'] = unique_grid.geometry.centroid
unique_grid['lon'] = unique_grid['centroid'].x
unique_grid['lat'] = unique_grid['centroid'].y

# Load temperature station data
temp = pd.read_csv("data/temp.csv", parse_dates=['date'])

# Extract unique weather stations
stations = temp[['station_id', 'lat', 'lon']].drop_duplicates().reset_index(drop=True)

# Print stations to confirm
print("Found", len(stations), "weather stations:")
print(stations)

# Prepare station coordinates for KDTree (lon, lat order!)
station_coords = stations[['lon', 'lat']].to_numpy()

# Function to assign nearest station via IDW
def idw_interpolation(lon, lat, stations, power=2):
    distances = np.sqrt((stations['lon'] - lon)**2 + (stations['lat'] - lat)**2)
    if np.any(distances == 0):
        return stations.loc[distances.idxmin(), 'station_id']
    weights = 1 / distances**power
    return stations.iloc[np.argmax(weights)]['station_id']

# Apply IDW to assign station to each grid cell
assigned_stations = []
for _, row in unique_grid.iterrows():
    sid = idw_interpolation(row['lon'], row['lat'], stations)
    assigned_stations.append(sid)

unique_grid['assigned_station_id'] = assigned_stations

# Merge assigned stations back into full final_grid
final_grid = final_grid.merge(
    unique_grid[['grid_id', 'assigned_station_id']],
    on='grid_id',
    how='left'
)

# Save updated grid with station assignments
final_grid.to_file("final_grid_with_stations.gpkg", driver="GPKG")

# Plot to visually confirm the station assignments look like CA
unique_grid['assigned_station_id'] = unique_grid['assigned_station_id'].astype(str)  # ensure categorical coloring
fig, ax = plt.subplots(figsize=(10, 10))
unique_grid.plot(ax=ax, column='assigned_station_id', cmap='tab20', edgecolor='k', linewidth=0.2, legend=False)
plt.title("Grid Cells Colored by Assigned Weather Station (IDW)")
plt.axis('equal')
plt.tight_layout()
plt.show()
