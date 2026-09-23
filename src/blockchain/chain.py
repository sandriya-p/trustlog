import json
import os
from src.blockchain.block import Block

CHAIN_FILE = "results/blockchain_data.json"


class Blockchain:
    def __init__(self):
        self.chain = []
        if os.path.exists(CHAIN_FILE):
            self.load_chain()
        else:
            self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(0, {"message": "Genesis Block"}, "0")
        self.chain.append(genesis)
        self.save_chain()

    def add_block(self, log_data):
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), log_data, previous_block.hash)
        self.chain.append(new_block)
        self.save_chain()
        return new_block

    def save_chain(self):
        with open(CHAIN_FILE, "w") as f:
            json.dump([b.to_dict() for b in self.chain], f, indent=2)

    def load_chain(self):
        with open(CHAIN_FILE, "r") as f:
            raw = json.load(f)
        self.chain = []
        for item in raw:
            b = Block.__new__(Block)
            b.index = item["index"]
            b.timestamp = item["timestamp"]
            b.log_data = item["log_data"]
            b.previous_hash = item["previous_hash"]
            b.hash = item["hash"]
            self.chain.append(b)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.compute_hash():
                return False, i
            if current.previous_hash != previous.hash:
                return False, i
        return True, None