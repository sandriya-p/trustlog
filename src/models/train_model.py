import time
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score

train_df = pd.read_csv("data/processed/features_train.csv")
test_df = pd.read_csv("data/processed/features_test.csv")

X_train = train_df.drop(columns=["label"])
y_train = train_df["label"]
X_test = test_df.drop(columns=["label"])
y_test = test_df["label"]

model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)

start = time.time()
model.fit(X_train, y_train)
train_time = time.time() - start

start = time.time()
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]
inference_time_ms = (time.time() - start) / len(X_test) * 1000

print(f"Training time: {train_time:.2f} seconds")
print(f"Inference latency: {inference_time_ms:.4f} ms/record")
print(f"Precision: {precision_score(y_test, y_pred):.4f}")
print(f"Recall:    {recall_score(y_test, y_pred):.4f}")
print(f"F1-score:  {f1_score(y_test, y_pred):.4f}")
print(f"ROC-AUC:   {roc_auc_score(y_test, y_proba):.4f}")

joblib.dump(model, "results/random_forest_model.joblib")
print("\nModel saved to results/random_forest_model.joblib")