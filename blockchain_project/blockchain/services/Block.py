from hashlib import sha256
import json
from datetime import datetime
from typing import List
from .Transaction import Transaction


class Block:
    def __init__(self, data: List[Transaction], previous_hash: str):
        self.data = data
        self.previous_hash = previous_hash
        self.timestamp = datetime.now()
        self.nonce: int = 0

    def serialize(self) -> str:
        return json.dumps({
            'data': self.data,
            'hash': self.get_hash(),
            'previous_hash': self.previous_hash,
            'timestamp': str(self.timestamp),
            'nonce': str(self.nonce),
        })

    def get_hash(self) -> str:
        return sha256(
            (str(self.data) + self.previous_hash + str(self.timestamp) + str(self.nonce)).encode()).hexdigest()

    def mine(self, difficulty: int):
        zeros = ''.join(['0' for zeros in range(0, difficulty)])
        while (self.get_hash()[0: difficulty] != zeros):
            self.nonce += 1
