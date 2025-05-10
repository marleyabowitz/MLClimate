import pandas as pd
import numpy as np
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

# Train base models
rf = RandomForestClassifier(class_weight='balanced', random_state=42)
xgb = XGBClassifier(eval_metric="logloss", use_label_encoder=False)

rf.fit(X_train, y_train)
xgb.fit(X_train, y_train)

rf_probs_train = rf.predict_proba(X_train)[:, 1]
xgb_probs_train = xgb.predict_proba(X_train)[:, 1]

rf_probs_test = rf.predict_proba(X_test)[:, 1]
xgb_probs_test = xgb.predict_proba(X_test)[:, 1]

# Ensemble methods
def evaluate_preds(name, y_true, y_probs, threshold=0.5):
    y_pred = (y_probs >= threshold).astype(int)
    print(f"\n🚀 {name}")
    print(f"✅ Threshold: {threshold}")
    print(f"F1 Score: {f1_score(y_true, y_pred):.4f}")
    print(f"Precision: {precision_score(y_true, y_pred, zero_division=0):.4f}")
    print(f"Recall: {recall_score(y_true, y_pred, zero_division=0):.4f}")
    print(f"ROC AUC: {roc_auc_score(y_true, y_probs):.4f}")
    print(f"🧮 Confusion Matrix:\n{confusion_matrix(y_true, y_pred)}")

# 1. Soft Voting (Simple average)
soft_vote_probs = (rf_probs_test + xgb_probs_test) / 2
evaluate_preds("Soft Voting (Average)", y_test, soft_vote_probs)

# 2. Weighted Voting
weighted_vote_probs = 0.7 * rf_probs_test + 0.3 * xgb_probs_test
evaluate_preds("Weighted Voting (70% RF, 30% XGB)", y_test, weighted_vote_probs)

# 3. Meta Model (Stacking)
meta_train = pd.DataFrame({
    "rf": rf_probs_train,
    "xgb": xgb_probs_train
})
meta_test = pd.DataFrame({
    "rf": rf_probs_test,
    "xgb": xgb_probs_test
})
meta_model = LogisticRegression()
meta_model.fit(meta_train, y_train)
meta_probs = meta_model.predict_proba(meta_test)[:, 1]
evaluate_preds("Stacked Model (LogReg on RF + XGB)", y_test, meta_probs)

# 4. Confidence-Aware Selection
confident_preds = []
for r, x in zip(rf_probs_test, xgb_probs_test):
    if abs(r - 0.5) > abs(x - 0.5):
        confident_preds.append(int(r >= 0.5))
    else:
        confident_preds.append(int(x >= 0.5))

# You need to use the *higher* of the two probabilities for AUC score
combined_probs = np.maximum(rf_probs_test, xgb_probs_test)
evaluate_preds("Confidence-Aware Model", y_test, combined_probs)
