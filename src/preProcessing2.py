import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

import xgboost as xgb
import lightgbm as lgb

from sklearn.inspection import permutation_importance
from sklearn.metrics import accuracy_score

# 1. Load Data
df = pd.read_csv("dataPreScaling.csv")

# 2. Drop Non-Predictive Columns
df = df.drop(columns=["grid_id", "county", "station_id", "week_start"])

# 3. Define Features and Target
X = df.drop(columns=["fire_occurred"])
y = df["fire_occurred"]

# 4. Scale Features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)

# 5. Correlation Matrix
plt.figure(figsize=(12, 10))
corr_matrix = X_scaled_df.corr()
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", square=True)
plt.title("Feature Correlation Matrix")
plt.tight_layout()
plt.show()

# 6. Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X_scaled_df, y, test_size=0.2, random_state=42)

# 7. XGBoost Classifier
xgb_model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
xgb_model.fit(X_train, y_train)

# XGBoost Feature Importance
xgb_importances = pd.Series(xgb_model.feature_importances_, index=X.columns).sort_values(ascending=False)

# Plot XGBoost Feature Importance
plt.figure(figsize=(10, 6))
sns.barplot(x=xgb_importances.values, y=xgb_importances.index)
plt.title("XGBoost Feature Importance")
plt.xlabel("Importance Score")
plt.ylabel("Features")
plt.tight_layout()
plt.show()

# 8. LightGBM Classifier
lgb_model = lgb.LGBMClassifier(random_state=42)
lgb_model.fit(X_train, y_train)

# LightGBM Feature Importance
lgb_importances = pd.Series(lgb_model.feature_importances_, index=X.columns).sort_values(ascending=False)

# Plot LightGBM Feature Importance
plt.figure(figsize=(10, 6))
sns.barplot(x=lgb_importances.values, y=lgb_importances.index)
plt.title("LightGBM Feature Importance")
plt.xlabel("Importance Score")
plt.ylabel("Features")
plt.tight_layout()
plt.show()


# 9. Permutation Importance for XGBoost
result_xgb = permutation_importance(
    xgb_model, X_test, y_test, n_repeats=10, random_state=42, scoring='accuracy'
)

# Sort and plot
perm_sorted_idx_xgb = result_xgb.importances_mean.argsort()[::-1]
plt.figure(figsize=(10, 6))
sns.barplot(
    x=result_xgb.importances_mean[perm_sorted_idx_xgb],
    y=X.columns[perm_sorted_idx_xgb]
)
plt.title("Permutation Importance - XGBoost")
plt.xlabel("Mean Decrease in Accuracy")
plt.ylabel("Features")
plt.tight_layout()
plt.show()

# 10. Permutation Importance for LightGBM
result_lgb = permutation_importance(
    lgb_model, X_test, y_test, n_repeats=10, random_state=42, scoring='accuracy'
)

# Sort and plot
perm_sorted_idx_lgb = result_lgb.importances_mean.argsort()[::-1]
plt.figure(figsize=(10, 6))
sns.barplot(
    x=result_lgb.importances_mean[perm_sorted_idx_lgb],
    y=X.columns[perm_sorted_idx_lgb]
)
plt.title("Permutation Importance - LightGBM")
plt.xlabel("Mean Decrease in Accuracy")
plt.ylabel("Features")
plt.tight_layout()
plt.show()