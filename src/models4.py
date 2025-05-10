import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import shap

from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score, confusion_matrix
from sklearn.model_selection import TimeSeriesSplit

# load data
train = pd.read_csv("train_data.csv")
test = pd.read_csv("test_data.csv")

X_train = train.drop(columns=["fire_occurred"])
y_train = train["fire_occurred"]
X_test = test.drop(columns=["fire_occurred"])
y_test = test["fire_occurred"]


run_cv = True 
if run_cv:
    tscv = TimeSeriesSplit(n_splits=5)
    f1_scores, precisions, recalls, roc_aucs = [], [], [], []

    fold = 1
    for train_index, val_index in tscv.split(X_train):
        X_tr, X_val = X_train.iloc[train_index], X_train.iloc[val_index]
        y_tr, y_val = y_train.iloc[train_index], y_train.iloc[val_index]

        # train models
        rf = RandomForestClassifier(class_weight='balanced', random_state=42)
        xgb = XGBClassifier(eval_metric="logloss", use_label_encoder=False, random_state=42)

        rf.fit(X_tr, y_tr)
        xgb.fit(X_tr, y_tr)

        # probabilities
        rf_probs = rf.predict_proba(X_val)[:, 1]
        xgb_probs = xgb.predict_proba(X_val)[:, 1]

        # Confidence-Aware Predictions
        preds = [int(r >= 0.5) if abs(r - 0.5) > abs(x - 0.5) else int(x >= 0.5)
                 for r, x in zip(rf_probs, xgb_probs)]
        combined_probs = np.maximum(rf_probs, xgb_probs)

        # evaluation
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

    print("\Average Cross Validation Results:")
    print(f"Average F1 Score: {np.mean(f1_scores):.4f}")
    print(f"Average Precision: {np.mean(precisions):.4f}")
    print(f"Average Recall: {np.mean(recalls):.4f}")
    print(f"Average ROC AUC: {np.mean(roc_aucs):.4f}")
