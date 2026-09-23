import os
import sys
sys.path.append(os.getcwd())

from src.blockchain.chain import Blockchain, CHAIN_FILE

if os.path.exists(CHAIN_FILE):
    os.remove(CHAIN_FILE)

bc = Blockchain()

sample_logs = [
    {"raw_description": "Normal connection from 192.168.1.5", "is_anomaly": 0},
    {"raw_description": "Repeated failed logins from 10.0.0.9", "is_anomaly": 1},
    {"raw_description": "Normal connection from 192.168.1.7", "is_anomaly": 0},
    {"raw_description": "Port scan detected from 172.16.0.3", "is_anomaly": 1},
    {"raw_description": "Normal connection from 192.168.1.10", "is_anomaly": 0},
]

for log in sample_logs:
    bc.add_block(log)

print(f"Chain now has {len(bc.chain)} blocks (including genesis).")
valid, idx = bc.is_chain_valid()
print(f"Chain valid: {valid}")