import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt
import seaborn as sns

# load, drop, define features and targets, scale, train/test split
df = pd.read_csv("dataPreScaling.csv")

df = df.drop(columns=["grid_id", "county", "station_id", "week_start"])

X = df.drop(columns=["fire_occurred"])
y = df["fire_occurred"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)

X_train, X_test, y_train, y_test = train_test_split(X_scaled_df, y, test_size=0.2, random_state=42)

# rf feature importance
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
rf_importances = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)

# logistic regression feature importance (this was very inaccurate and I didn't include it in the report)
lr = LogisticRegression(max_iter=1000)
lr.fit(X_train, y_train)
lr_importances = pd.Series(abs(lr.coef_[0]), index=X.columns).sort_values(ascending=False)

# rf permutation importance
perm_importance = permutation_importance(rf, X_test, y_test, n_repeats=10, random_state=42)
perm_sorted = pd.Series(perm_importance.importances_mean, index=X.columns).sort_values(ascending=False)

# results
print("\nRandom Forest Feature Importance")
print(rf_importances)

print("\nLogistic Regression Coefficients (absolute)")
print(lr_importances)

print("\nPermutation Importance")
print(perm_sorted)

# plot
plt.figure(figsize=(10, 6))
sns.barplot(x=rf_importances.values, y=rf_importances.index)
plt.title("Random Forest Feature Importance")
plt.tight_layout()
plt.show()
