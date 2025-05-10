import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import shap
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score, confusion_matrix

# Load data
train = pd.read_csv("train_data.csv")
test = pd.read_csv("test_data.csv")

X_train = train.drop(columns=["fire_occurred"])
y_train = train["fire_occurred"]
X_test = test.drop(columns=["fire_occurred"])
y_test = test["fire_occurred"]

# Train models
rf = RandomForestClassifier(class_weight='balanced', random_state=42)
xgb = XGBClassifier(eval_metric="logloss", use_label_encoder=False, random_state=42)

rf.fit(X_train, y_train)
xgb.fit(X_train, y_train)

# Predict probabilities
rf_probs_test = rf.predict_proba(X_test)[:, 1]
xgb_probs_test = xgb.predict_proba(X_test)[:, 1]

# Confidence-Aware Prediction
confident_preds = []
for r, x in zip(rf_probs_test, xgb_probs_test):
    if abs(r - 0.5) > abs(x - 0.5):
        confident_preds.append(int(r >= 0.5))
    else:
        confident_preds.append(int(x >= 0.5))

confident_preds = np.array(confident_preds)
combined_probs = np.maximum(rf_probs_test, xgb_probs_test)

# Evaluation
print("\n🚀 Confidence-Aware Model Results")
print(f"F1 Score: {f1_score(y_test, confident_preds):.4f}")
print(f"Precision: {precision_score(y_test, confident_preds, zero_division=0):.4f}")
print(f"Recall: {recall_score(y_test, confident_preds, zero_division=0):.4f}")
print(f"ROC AUC: {roc_auc_score(y_test, combined_probs):.4f}")
print(f"🧮 Confusion Matrix:\n{confusion_matrix(y_test, confident_preds)}")

# ---------------------------------------------
# Feature Importance
# ---------------------------------------------

features = X_train.columns

# Random Forest
feat_importances_rf = pd.Series(rf.feature_importances_, index=features).sort_values(ascending=False)
plt.figure(figsize=(10,6))
sns.barplot(x=feat_importances_rf.values, y=feat_importances_rf.index)
plt.title('Random Forest Feature Importances')
plt.show()

# XGBoost
feat_importances_xgb = pd.Series(xgb.feature_importances_, index=features).sort_values(ascending=False)
plt.figure(figsize=(10,6))
sns.barplot(x=feat_importances_xgb.values, y=feat_importances_xgb.index)
plt.title('XGBoost Feature Importances')
plt.show()

# ---------------------------------------------
# SHAP Explainability
# ---------------------------------------------

explainer = shap.TreeExplainer(xgb)
shap_values = explainer.shap_values(X_test)

# SHAP Summary Plot
shap.summary_plot(shap_values, X_test)

# ---------------------------------------------
# Error Analysis
# ---------------------------------------------

# Add predictions to test dataframe
test['y_true'] = y_test
test['y_pred'] = confident_preds
test['rf_prob'] = rf_probs_test
test['xgb_prob'] = xgb_probs_test
test['combined_prob'] = combined_probs

false_positives = test[(test['y_true'] == 0) & (test['y_pred'] == 1)]
false_negatives = test[(test['y_true'] == 1) & (test['y_pred'] == 0)]

print("\n🔎 False Positives (predicted fire but no fire):")
print(false_positives)

print("\n🔎 False Negatives (missed actual fire):")
print(false_negatives)