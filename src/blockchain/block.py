import hashlib
import json
from datetime import datetime, timezone


class Block:
    def __init__(self, index, log_data, previous_hash):
        self.index = index
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.log_data = log_data
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_content = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "log_data": self.log_data,
            "previous_hash": self.previous_hash,
        }, sort_keys=True)
        return hashlib.sha256(block_content.encode()).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "log_data": self.log_data,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
        }