import json
import os
import sys
sys.path.append(os.getcwd())

from src.blockchain.chain import Blockchain, CHAIN_FILE

print("=== BEFORE TAMPERING ===")
bc = Blockchain()
valid, idx = bc.is_chain_valid()
print(f"Chain valid: {valid}")

print("\nSimulating an attacker directly editing the stored log file "
      "(bypassing the application entirely)...")

with open(CHAIN_FILE, "r") as f:
    data = json.load(f)

# Block index 2 = "Repeated failed logins from 10.0.0.9"
# Attacker flips is_anomaly from 1 to 0.
data[2]["log_data"]["is_anomaly"] = 0

with open(CHAIN_FILE, "w") as f:
    json.dump(data, f, indent=2)

print("\n=== AFTER TAMPERING ===")
bc2 = Blockchain()
valid2, idx2 = bc2.is_chain_valid()
print(f"Chain valid: {valid2}")

if not valid2:
    print(f"Tampering detected at block index: {idx2}")