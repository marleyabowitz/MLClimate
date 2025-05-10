import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt

# Load data
fire_df = pd.read_csv('fireData_with_climate_and_population.csv')
incident_df = pd.read_csv('data/mapdataall.csv')

# Convert fire date and grid week_start to datetime
incident_df['incident_dateonly_created'] = pd.to_datetime(incident_df['incident_dateonly_created'], errors='coerce')
fire_df['week_start'] = pd.to_datetime(fire_df['week_start'], errors='coerce')

# Drop rows without location info
incident_df = incident_df.dropna(subset=['incident_latitude', 'incident_longitude'])

# Parse lat/lon from grid_id
fire_df[['lat', 'lon']] = fire_df['grid_id'].str.split('_', expand=True).astype(float)

# Helper: haversine distance
def haversine(lon1, lat1, lon2, lat2):
    R = 6371  # Earth radius in km
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    return 2 * R * asin(sqrt(a))

# Helper: estimate radius in km from acres
def acres_to_radius_km(acres):
    if pd.isna(acres) or acres == 0:
        return 2  # Assume minimum radius
    return sqrt(acres / np.pi) * 0.0636  # Based on conversion to km²

# Initialize binary column
fire_df['fire_occurred'] = 0

# Iterate over incidents
for _, incident in incident_df.iterrows():
    lat = incident['incident_latitude']
    lon = incident['incident_longitude']
    date = incident['incident_dateonly_created']
    acres = incident.get('incident_acres_burned', 0)

    radius_km = acres_to_radius_km(acres)

    # Filter week_start == incident week
    week_mask = fire_df['week_start'] == date
    df_in_week = fire_df[week_mask].copy()

    for idx, row in df_in_week.iterrows():
        dist = haversine(lon, lat, row['lon'], row['lat'])
        if dist <= radius_km:
            fire_df.at[idx, 'fire_occurred'] = 1

# Create fire_past_year
fire_df['fire_past_year'] = 0
fire_df.sort_values(['grid_id', 'week_start'], inplace=True)

# For each grid_id, mark if any of previous 52 weeks had fire
from collections import deque
for grid_id, group in fire_df.groupby('grid_id'):
    history = deque()
    past_year_flags = []
    for _, row in group.iterrows():
        # Remove old entries
        history = deque([d for d in history if (row['week_start'] - d).days <= 365])
        past_year_flags.append(1 if history else 0)
        if row['fire_occurred'] == 1:
            history.append(row['week_start'])
    fire_df.loc[group.index, 'fire_past_year'] = past_year_flags

# Save result
fire_df.to_csv('fireDataPreProcessing.csv', index=False)
print("✅ Done! Output written to fireDataPreProcessing.csv")
