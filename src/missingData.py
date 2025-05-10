import pandas as pd

# === Step 1: Load CSV ===
# Replace with your actual file path
file_path = "fireDataPreProcessing.csv"
df = pd.read_csv(file_path)

# === Step 2: Report Missing Values ===
print("Missing values per column:")
missing_counts = df.isna().sum()
for col, count in missing_counts.items():
    if count > 0:
        print(f"{col}: {count}")

# === Step 3: Drop 'wdir' column ===
if 'wdir' in df.columns:
    df = df.drop(columns=['wdir'])
    print("\nDropped 'wdir' column due to high missing values.")

# === Step 4: Impute 'tavg' and 'wspd' using group mean ===

# Group by 'grid_id' and fill with group mean
for col in ['tavg', 'wspd']:
    if col in df.columns:
        df[col] = df.groupby('grid_id')[col].transform(lambda x: x.fillna(x.mean()))
        # Fill remaining NaNs with global mean
        df[col] = df[col].fillna(df[col].mean())
        print(f"Filled missing values in '{col}' using group and global means.")

# === Step 5: Final Check ===
print("\nMissing values after cleaning:")
final_missing = df.isna().sum()
for col, count in final_missing.items():
    if count > 0:
        print(f"{col}: {count}")
    else:
        continue

# === Step 6: Save cleaned data ===
output_file = "cleaned_fire_data.csv"
df.to_csv(output_file, index=False)
print(f"\nCleaned dataset saved to '{output_file}'")
