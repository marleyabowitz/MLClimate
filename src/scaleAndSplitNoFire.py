import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load dataset
df = pd.read_csv("dataPreScaling.csv")

# Drop unwanted columns
df = df.drop(columns=["grid_id", "county", "station_id", "week_start", "fire_past_year"])

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

# Split the data
train_df, test_df = train_test_split(final_df, test_size=0.2, random_state=42, stratify=y)

# Save to CSV
train_df.to_csv("train_data_noFire.csv", index=False)
test_df.to_csv("test_data_noFire.csv", index=False)

print("Preprocessing complete. Files saved: train_data.csv and test_data.csv")
