import pandas as pd

# 1. Load and filter fireData
fire = pd.read_csv("fireData.csv", parse_dates=["week_start"])

# Shift every week_start one day earlier
fire["week_start"] = fire["week_start"] - pd.Timedelta(days=1)


# Drop any grid cells not on the CA map
fire = fire[fire["county"].notna()].reset_index(drop=True)


# 2. Load weather data
# Note: each weather file has columns: station_id, date, <value>
temp = pd.read_csv("data/temp.csv", parse_dates=["date"])
wdir = pd.read_csv("data/windDirection.csv", parse_dates=["date"])
wspd = pd.read_csv("data/windSpeed.csv", parse_dates=["date"])

# 3. Align column names for merging
for df in (temp, wdir, wspd):
    df.rename(columns={"date": "week_start"}, inplace=True)

# 4. Merge weather into fireData
#    We’ll merge one at a time on ['station_id', 'week_start']
fire = fire.merge(
    temp[["station_id", "week_start", "tavg"]],
    on=["station_id", "week_start"],
    how="left"
)
fire = fire.merge(
    wdir[["station_id", "week_start", "wdir"]],
    on=["station_id", "week_start"],
    how="left"
)
fire = fire.merge(
    wspd[["station_id", "week_start", "wspd"]],
    on=["station_id", "week_start"],
    how="left"
)

# 5. (Optional) Reorder columns for clarity
cols = [
    "grid_id", "county", "station_id", "week_start",
    "tavg", "wdir", "wspd"
]
# keep any other columns at the end
other_cols = [c for c in fire.columns if c not in cols]
fire = fire[cols + other_cols]

# 6. Save the enriched CSV
fire.to_csv("fireData.csv", index=False)

print(f"Done! {len(fire)} rows written to fireData.csv")