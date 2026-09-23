import pandas as pd

columns = [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes", "land",
    "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in", "num_compromised",
    "root_shell", "su_attempted", "num_root", "num_file_creations", "num_shells",
    "num_access_files", "num_outbound_cmds", "is_host_login", "is_guest_login", "count",
    "srv_count", "serror_rate", "srv_serror_rate", "rerror_rate", "srv_rerror_rate",
    "same_srv_rate", "diff_srv_rate", "srv_diff_host_rate", "dst_host_count",
    "dst_host_srv_count", "dst_host_same_srv_rate", "dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate", "dst_host_serror_rate",
    "dst_host_srv_serror_rate", "dst_host_rerror_rate", "dst_host_srv_rerror_rate",
    "attack_type", "difficulty_level",
]

train_df = pd.read_csv("data/raw/KDDTrain+.txt", names=columns)
test_df = pd.read_csv("data/raw/KDDTest+.txt", names=columns)

print("Train shape:", train_df.shape)
print("Test shape:", test_df.shape)
print(train_df.head())
print("\nTop attack types in training data:")
print(train_df["attack_type"].value_counts().head(10))

train_df.to_csv("data/processed/train_raw.csv", index=False)
test_df.to_csv("data/processed/test_raw.csv", index=False)