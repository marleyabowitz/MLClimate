import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import box
from datetime import datetime
import matplotlib.pyplot as plt

# load county shapefile
counties = gpd.read_file("boundries.shp").to_crs(epsg=4326)

# create box of CA
minx, miny, maxx, maxy = counties.total_bounds

# create 0.1° x 0.1° grid
lat_steps = np.arange(miny, maxy, 0.1)
lon_steps = np.arange(minx, maxx, 0.1)
grid_cells = [box(x, y, x + 0.1, y + 0.1) for x in lon_steps for y in lat_steps]
grid = gpd.GeoDataFrame({'geometry': grid_cells}, crs='EPSG:4326')

# assign grid IDs with centroid coordinates
grid_proj = grid.to_crs(epsg=3310)
centroids = grid_proj.geometry.centroid.to_crs(epsg=4326)
grid['lat'] = centroids.y.round(4)
grid['lon'] = centroids.x.round(4)
grid['grid_id'] = grid['lat'].astype(str) + "_" + grid['lon'].astype(str)

# assign counties to grid cells

grid_with_counties = gpd.sjoin(grid, counties[['geometry', 'CDT_COUNTY']], how='left', predicate='intersects')
grid_with_counties = grid_with_counties.rename(columns={'CDT_COUNTY': 'county'}).drop(columns='index_right')

# load the weather stations (using temp)
temp = pd.read_csv("data/temp.csv", parse_dates=['date'])
stations = temp[['station_id', 'lat', 'lon']].drop_duplicates().reset_index(drop=True)

# IDW interpolation
def idw_interpolation(lon, lat, stations, power=2):
    distances = np.sqrt((stations['lon'] - lon)**2 + (stations['lat'] - lat)**2)
    if np.any(distances == 0):
        return stations.loc[distances.idxmin(), 'station_id']
    weights = 1 / distances**power
    return stations.iloc[np.argmax(weights)]['station_id']

assigned_stations = [
    idw_interpolation(row['lon'], row['lat'], stations)
    for _, row in grid_with_counties.iterrows()
]
grid_with_counties['station_id'] = assigned_stations

# weekly time series

weeks = pd.date_range(start="2014-01-01", end="2024-12-31", freq="W-MON")
time_index = pd.MultiIndex.from_product(
    [grid_with_counties['grid_id'], weeks],
    names=['grid_id', 'week_start']
)
grid_time_df = pd.DataFrame(index=time_index).reset_index()

# combine and save

meta = grid_with_counties[['grid_id', 'county', 'station_id']].drop_duplicates()
fire_data = grid_time_df.merge(meta, on='grid_id', how='left')
fire_data = fire_data[['grid_id', 'county', 'station_id', 'week_start']]
fire_data.to_csv("fireData.csv", index=False)


# plotting!

# grid by county, with unassigned cells left white
fig, ax = plt.subplots(figsize=(10, 10))

grid_with_counties[grid_with_counties['county'].notna()] \
    .plot(
    ax=ax,
    column='county',
    cmap='tab20',
    edgecolor='black',
    linewidth=0.2,
    legend=False
)

grid_with_counties[grid_with_counties['county'].isna()] \
    .plot(
    ax=ax,
    color='white',
    edgecolor='black',
    linewidth=0.2
)

plt.title("Grid Cells Colored by County (Unassigned Cells in White)")
plt.axis('equal')
plt.tight_layout()
plt.show()

# grid by assigned weather station
fig, ax = plt.subplots(figsize=(10, 10))
grid_with_counties.plot(
    ax=ax, column='station_id', cmap='tab20', edgecolor='black', linewidth=0.2
)
plt.title("Grid Cells Colored by Assigned Weather Station")
plt.axis('equal')
plt.tight_layout()
plt.show()
