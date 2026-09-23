import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score
from tensorflow import keras

train_df = pd.read_csv("data/processed/features_train.csv")
test_df = pd.read_csv("data/processed/features_test.csv")

X_train = train_df.drop(columns=["label"]).values
y_train = train_df["label"].values
X_test = test_df.drop(columns=["label"]).values
y_test = test_df["label"].values

results = []

def evaluate(name, y_true, y_pred, y_score, train_time, infer_ms):
    results.append({
        "Algorithm": name,
        "Precision": round(precision_score(y_true, y_pred, zero_division=0), 4),
        "Recall": round(recall_score(y_true, y_pred, zero_division=0), 4),
        "F1": round(f1_score(y_true, y_pred, zero_division=0), 4),
        "ROC_AUC": round(roc_auc_score(y_true, y_score), 4),
        "Train_Time_sec": round(train_time, 2),
        "Inference_ms_per_record": round(infer_ms, 4),
    })

# 1. Logistic Regression — simple linear baseline
model = LogisticRegression(max_iter=500)
t0 = time.time(); model.fit(X_train, y_train); t_train = time.time() - t0
t0 = time.time(); y_pred = model.predict(X_test); y_score = model.predict_proba(X_test)[:, 1]
t_infer = (time.time() - t0) / len(X_test) * 1000
evaluate("Logistic Regression", y_test, y_pred, y_score, t_train, t_infer)

# 2. Random Forest — strong classical baseline (same as Day 4)
model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
t0 = time.time(); model.fit(X_train, y_train); t_train = time.time() - t0
t0 = time.time(); y_pred = model.predict(X_test); y_score = model.predict_proba(X_test)[:, 1]
t_infer = (time.time() - t0) / len(X_test) * 1000
evaluate("Random Forest", y_test, y_pred, y_score, t_train, t_infer)

# 3. Isolation Forest — unsupervised anomaly detector
model = IsolationForest(contamination=0.46, random_state=42, n_jobs=-1)
t0 = time.time(); model.fit(X_train); t_train = time.time() - t0
t0 = time.time()
raw_pred = model.predict(X_test)                       # -1 = anomaly, 1 = normal
y_pred = np.where(raw_pred == -1, 1, 0)
y_score = -model.decision_function(X_test)              # higher = more anomalous
t_infer = (time.time() - t0) / len(X_test) * 1000
evaluate("Isolation Forest", y_test, y_pred, y_score, t_train, t_infer)

# 4. One-Class SVM — unsupervised, trained only on a NORMAL sample
# (SVMs don't scale well to 125k rows, so we sample 5,000 normal records)
normal_sample = train_df[train_df["label"] == 0].drop(columns=["label"]).sample(n=5000, random_state=42)
model = OneClassSVM(kernel="rbf", nu=0.1, gamma="scale")
t0 = time.time(); model.fit(normal_sample); t_train = time.time() - t0
t0 = time.time()
raw_pred = model.predict(X_test)
y_pred = np.where(raw_pred == -1, 1, 0)
y_score = -model.decision_function(X_test)
t_infer = (time.time() - t0) / len(X_test) * 1000
evaluate("One-Class SVM", y_test, y_pred, y_score, t_train, t_infer)

# 5. Neural Network (MLP) — our "AI-driven" flagship deep learning model
nn = keras.Sequential([
    keras.layers.Input(shape=(X_train.shape[1],)),
    keras.layers.Dense(64, activation="relu"),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(32, activation="relu"),
    keras.layers.Dense(1, activation="sigmoid"),
])
nn.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
t0 = time.time()
nn.fit(X_train, y_train, epochs=10, batch_size=256, verbose=0, validation_split=0.1)
t_train = time.time() - t0
t0 = time.time()
y_score = nn.predict(X_test, verbose=0).ravel()
y_pred = (y_score >= 0.5).astype(int)
t_infer = (time.time() - t0) / len(X_test) * 1000
evaluate("Neural Network (MLP)", y_test, y_pred, y_score, t_train, t_infer)

results_df = pd.DataFrame(results)
results_df.to_csv("results/comparison_table.csv", index=False)
print(results_df.to_string(index=False))

plt.figure(figsize=(8, 5))
plt.bar(results_df["Algorithm"], results_df["F1"], color="steelblue")
plt.ylabel("F1-score")
plt.title("Model Comparison — F1-score on NSL-KDD Test Set")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig("results/model_comparison_f1.png")
print("\nSaved: results/comparison_table.csv and results/model_comparison_f1.png")