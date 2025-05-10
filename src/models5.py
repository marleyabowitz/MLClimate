import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import shap

from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score, confusion_matrix
from sklearn.model_selection import TimeSeriesSplit

# Load data
train = pd.read_csv("train_data.csv")
test = pd.read_csv("test_data.csv")

X_train = train.drop(columns=["fire_occurred"])
y_train = train["fire_occurred"]
X_test = test.drop(columns=["fire_occurred"])
y_test = test["fire_occurred"]

# ---------------------------------------------
# Optional: Time Series Cross Validation
# ---------------------------------------------
run_cv = True  # Toggle this to enable/disable CV

if run_cv:
    tscv = TimeSeriesSplit(n_splits=5)
    f1_scores, precisions, recalls, roc_aucs = [], [], [], []

    fold = 1
    for train_index, val_index in tscv.split(X_train):
        X_tr, X_val = X_train.iloc[train_index], X_train.iloc[val_index]
        y_tr, y_val = y_train.iloc[train_index], y_train.iloc[val_index]

        # Train models for this fold
        rf = RandomForestClassifier(class_weight='balanced', random_state=42)
        xgb = XGBClassifier(eval_metric="logloss", use_label_encoder=False, random_state=42)

        rf.fit(X_tr, y_tr)
        xgb.fit(X_tr, y_tr)

        # Predict probabilities
        rf_probs = rf.predict_proba(X_val)[:, 1]
        xgb_probs = xgb.predict_proba(X_val)[:, 1]

        # Confidence-Aware Predictions
        preds = [int(r >= 0.5) if abs(r - 0.5) > abs(x - 0.5) else int(x >= 0.5)
                 for r, x in zip(rf_probs, xgb_probs)]
        combined_probs = np.maximum(rf_probs, xgb_probs)

        # Metrics
        f1_scores.append(f1_score(y_val, preds))
        precisions.append(precision_score(y_val, preds, zero_division=0))
        recalls.append(recall_score(y_val, preds, zero_division=0))
        roc_aucs.append(roc_auc_score(y_val, combined_probs))

        print(f"\nFold {fold} Results:")
        print(f"F1 Score: {f1_scores[-1]:.4f}")
        print(f"Precision: {precisions[-1]:.4f}")
        print(f"Recall: {recalls[-1]:.4f}")
        print(f"ROC AUC: {roc_aucs[-1]:.4f}")
        fold += 1

    print("\n🚀 Average Cross Validation Results:")
    print(f"Average F1 Score: {np.mean(f1_scores):.4f}")
    print(f"Average Precision: {np.mean(precisions):.4f}")
    print(f"Average Recall: {np.mean(recalls):.4f}")
    print(f"Average ROC AUC: {np.mean(roc_aucs):.4f}")

# ---------------------------------------------
# Final Model Training on Full Training Data
# ---------------------------------------------
rf = RandomForestClassifier(class_weight='balanced', random_state=42)
xgb = XGBClassifier(eval_metric="logloss", use_label_encoder=False, random_state=42)

rf.fit(X_train, y_train)
xgb.fit(X_train, y_train)

# Predict on test set
rf_probs_test = rf.predict_proba(X_test)[:, 1]
xgb_probs_test = xgb.predict_proba(X_test)[:, 1]

# Confidence-Aware Test Prediction
confident_preds = [int(r >= 0.5) if abs(r - 0.5) > abs(x - 0.5) else int(x >= 0.5)
                   for r, x in zip(rf_probs_test, xgb_probs_test)]
confident_preds = np.array(confident_preds)
combined_probs = np.maximum(rf_probs_test, xgb_probs_test)

# Test Evaluation
print("\n🚀 Confidence-Aware Model Results on Test Set")
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

shap.summary_plot(shap_values, X_test)

# ---------------------------------------------
# Error Analysis
# ---------------------------------------------
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