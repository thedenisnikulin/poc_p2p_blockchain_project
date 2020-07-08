import sys
import json
from hashlib import sha256
from datetime import datetime
from typing import List
# local
from Transaction import Transaction


class Block:
    def __init__(self, transactions: List, previous_hash: str):
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = datetime.now()
        self.nonce: int = 0

    @property
    def serialized(self) -> dict:
        return {
            'transactions': self.transactions,
            'hash': self.get_hash(),
            'previous_hash': self.previous_hash,
            'timestamp': str(self.timestamp),
            'nonce': str(self.nonce),
        }

    def get_hash(self) -> str:
        return sha256(
            (str(self.transactions) + self.previous_hash + str(self.timestamp) + str(self.nonce)).encode()).hexdigest()

    def mine(self, difficulty: int):
        zeros = ''.join(['0' for o in range(0, difficulty)])
        while self.get_hash()[0: difficulty] != zeros:
            self.nonce += 1
        print('\n')