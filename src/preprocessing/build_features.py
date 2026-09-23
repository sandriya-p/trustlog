import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

train_df = pd.read_csv("data/processed/train_raw.csv")
test_df = pd.read_csv("data/processed/test_raw.csv")

# Binary label: 0 = normal, 1 = attack (of any kind)
train_df["label"] = train_df["attack_type"].apply(lambda x: 0 if x == "normal" else 1)
test_df["label"] = test_df["attack_type"].apply(lambda x: 0 if x == "normal" else 1)

# Encode the 3 categorical columns using the same encoder fit on both sets
categorical_cols = ["protocol_type", "service", "flag"]
for col in categorical_cols:
    le = LabelEncoder()
    le.fit(pd.concat([train_df[col], test_df[col]]))
    train_df[col] = le.transform(train_df[col])
    test_df[col] = le.transform(test_df[col])

train_df = train_df.drop(columns=["attack_type", "difficulty_level"])
test_df = test_df.drop(columns=["attack_type", "difficulty_level"])

# Scale all numeric feature columns to mean 0, std 1
feature_cols = [c for c in train_df.columns if c != "label"]
scaler = StandardScaler()
train_df[feature_cols] = scaler.fit_transform(train_df[feature_cols])
test_df[feature_cols] = scaler.transform(test_df[feature_cols])

train_df.to_csv("data/processed/features_train.csv", index=False)
test_df.to_csv("data/processed/features_test.csv", index=False)

print("Final training feature table shape:", train_df.shape)
print("\nNormal vs Attack counts (train):")
print(train_df["label"].value_counts())