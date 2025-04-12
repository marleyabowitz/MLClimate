import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import box
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Load the California counties shapefile
counties = gpd.read_file("boundries.shp")
counties = counties.to_crs(epsg=4326)  # Ensure it's in WGS84

# Define the bounding box for California
minx, miny, maxx, maxy = counties.total_bounds

# Create a 0.1° x 0.1° grid
grid_cells = []
lat_steps = np.arange(miny, maxy, 0.1)
lon_steps = np.arange(minx, maxx, 0.1)
for x in lon_steps:
    for y in lat_steps:
        grid_cells.append(box(x, y, x + 0.1, y + 0.1))

grid = gpd.GeoDataFrame({'geometry': grid_cells})
grid = grid.set_crs(epsg=4326)

# Spatial join to assign counties to grid cells
grid_with_counties = gpd.sjoin(grid, counties[['geometry', 'CDT_COUNTY']], how='left', predicate='intersects')
grid_with_counties = grid_with_counties.rename(columns={'CDT_COUNTY': 'county'}).drop(columns='index_right')

# Create weekly dates
start_date = datetime(2013, 1, 1)
end_date = datetime(2025, 3, 31)
weeks = pd.date_range(start=start_date, end=end_date, freq='W-MON')

# Create a DataFrame with all combinations of grid cells and weeks
grid_with_counties['grid_id'] = grid_with_counties.index
time_index = pd.MultiIndex.from_product([grid_with_counties['grid_id'], weeks], names=['grid_id', 'week_start'])
grid_time_df = pd.DataFrame(index=time_index).reset_index()

# Merge to get geometry and county information
final_grid = grid_time_df.merge(grid_with_counties[['grid_id', 'geometry', 'county']], on='grid_id', how='left')


# Drop duplicate geometries (per grid_id) and convert to GeoDataFrame
unique_geoms = final_grid[['grid_id', 'geometry', 'county']].drop_duplicates()
unique_geoms = gpd.GeoDataFrame(unique_geoms, geometry='geometry', crs="EPSG:4326")

# Plotting
fig, ax = plt.subplots(figsize=(10, 10))
unique_geoms.plot(ax=ax, column='county', legend=True, edgecolor='black', linewidth=0.2)
plt.title("California Grid Cells by County")
plt.show()

# Convert final_grid back to GeoDataFrame
final_grid = gpd.GeoDataFrame(final_grid, geometry='geometry', crs="EPSG:4326")

# Now save it
final_grid.to_file("final_grid.gpkg", driver="GPKG")