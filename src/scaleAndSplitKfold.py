import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler

# Load dataset
df = pd.read_csv("dataPreScaling.csv")

# Drop unwanted columns
df = df.drop(columns=["grid_id", "county", "station_id", "week_start"])

# Separate features and target
X = df.drop(columns=["fire_occurred"])
y = df["fire_occurred"]

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Create a DataFrame from scaled features
X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)

# Add target column back
final_df = X_scaled_df.copy()
final_df["fire_occurred"] = y.values

# Use first fold from StratifiedKFold as a deterministic train/test split
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
train_idx, test_idx = next(skf.split(X_scaled_df, y))

# Extract train/test data
train_df = final_df.iloc[train_idx]
test_df = final_df.iloc[test_idx]

# Save to CSV
train_df.to_csv("train_data_KFold.csv", index=False)
test_df.to_csv("test_data_KFold.csv", index=False)

print("Preprocessing complete. Files saved: train_data.csv and test_data.csv")