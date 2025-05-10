import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler

# load, drop, split, scale
df = pd.read_csv("dataPreScaling.csv")
df = df.drop(columns=["grid_id", "county", "station_id", "week_start"])

X = df.drop(columns=["fire_occurred"])
y = df["fire_occurred"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)

final_df = X_scaled_df.copy()
final_df["fire_occurred"] = y.values

# first fold from StratifiedKFold as a train/test split
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
train_idx, test_idx = next(skf.split(X_scaled_df, y))

# train/test data
train_df = final_df.iloc[train_idx]
test_df = final_df.iloc[test_idx]

# save csv
train_df.to_csv("train_data_KFold.csv", index=False)
test_df.to_csv("test_data_KFold.csv", index=False)

print("Preprocessing complete. Files saved: train_data.csv and test_data.csv")
