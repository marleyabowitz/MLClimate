import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt
import seaborn as sns

# === 1. Load Data ===
df = pd.read_csv("dataPreScaling.csv")

# === 2. Drop non-predictive or ID columns (but keep lat/lon) ===
df = df.drop(columns=["grid_id", "county", "station_id", "week_start"])

# === 3. Define Features and Target ===
X = df.drop(columns=["fire_occurred"])
y = df["fire_occurred"]

# === 4. Scale Features ===
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)

# === 5. Train/Test Split ===
X_train, X_test, y_train, y_test = train_test_split(X_scaled_df, y, test_size=0.2, random_state=42)

# === 6. Feature Importance via Random Forest ===
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
rf_importances = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)

# === 7. Feature Importance via Logistic Regression ===
lr = LogisticRegression(max_iter=1000)
lr.fit(X_train, y_train)
lr_importances = pd.Series(abs(lr.coef_[0]), index=X.columns).sort_values(ascending=False)

# === 8. Permutation Importance (on Random Forest) ===
perm_importance = permutation_importance(rf, X_test, y_test, n_repeats=10, random_state=42)
perm_sorted = pd.Series(perm_importance.importances_mean, index=X.columns).sort_values(ascending=False)

# === 9. Print Results ===
print("\n=== Random Forest Feature Importance ===")
print(rf_importances)

print("\n=== Logistic Regression Coefficients (absolute) ===")
print(lr_importances)

print("\n=== Permutation Importance ===")
print(perm_sorted)

# === 10. Optional: Plot Feature Importances ===
plt.figure(figsize=(10, 6))
sns.barplot(x=rf_importances.values, y=rf_importances.index)
plt.title("Random Forest Feature Importance")
plt.tight_layout()
plt.show()