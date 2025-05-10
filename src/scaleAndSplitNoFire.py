import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# load, drop, and split
df = pd.read_csv("dataPreScaling.csv")
df = df.drop(columns=["grid_id", "county", "station_id", "week_start", "fire_past_year"])

X = df.drop(columns=["fire_occurred"])
y = df["fire_occurred"]

# scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)

# target
final_df = X_scaled_df.copy()
final_df["fire_occurred"] = y.values

# split
train_df, test_df = train_test_split(final_df, test_size=0.2, random_state=42, stratify=y)

# save
train_df.to_csv("train_data_noFire.csv", index=False)
test_df.to_csv("test_data_noFire.csv", index=False)

print("Preprocessing complete. Files saved: train_data.csv and test_data.csv")
