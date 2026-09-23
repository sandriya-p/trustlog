import os
import sys
sys.path.append(os.getcwd())

from src.blockchain.chain import Blockchain, CHAIN_FILE


def test_valid_chain_detects_no_tampering():
    if os.path.exists(CHAIN_FILE):
        os.remove(CHAIN_FILE)
    bc = Blockchain()
    bc.add_block({"raw_log": "test log 1", "is_anomaly": 0})
    bc.add_block({"raw_log": "test log 2", "is_anomaly": 1})

    valid, tampered_index = bc.is_chain_valid()
    assert valid is True
    assert tampered_index is None


def test_tampering_is_detected():
    bc = Blockchain()
    bc.chain[1].log_data["is_anomaly"] = 999
    valid, tampered_index = bc.is_chain_valid()
    assert valid is False
    assert tampered_index == 1