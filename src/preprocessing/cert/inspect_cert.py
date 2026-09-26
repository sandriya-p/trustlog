import pandas as pd

BASE = "data/raw/CERT/r1"

# Load CERT r1 datasets
logon = pd.read_csv(f"{BASE}/logon.csv")

device = pd.read_csv(f"{BASE}/device.csv")

http = pd.read_csv(
    f"{BASE}/http.csv",
    header=None,
    names=["id", "date", "user", "pc", "url"]
)

ldap = pd.read_csv(f"{BASE}/LDAP/2009-12.csv")


# Display LOGON information
print("\n--- LOGON ---")
print("Shape:", logon.shape)
print("Columns:", logon.columns.tolist())
print(logon.head())


# Display DEVICE information
print("\n--- DEVICE ---")
print("Shape:", device.shape)
print("Columns:", device.columns.tolist())
print(device.head())


# Display HTTP information
print("\n--- HTTP ---")
print("Shape:", http.shape)
print("Columns:", http.columns.tolist())
print(http.head())


# Display LDAP information
print("\n--- LDAP ---")
print("Shape:", ldap.shape)
print("Columns:", ldap.columns.tolist())
print(ldap.head())