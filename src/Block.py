from hashlib import sha256
import json
from datetime import datetime

class Block():
    def __init__(self, data: dict, previous_hash: str):
        self.data = data
        self.previous_hash = previous_hash
        self.timestamp = datetime.now()
        self.nonce = 0
    
    def serialize(self) -> str:
        return json.dumps({
            'data': self.data,
            'hash': self.get_hash(),
            'previous_hash': self.previous_hash,
            'timestamp': str(self.timestamp),
            'nonce': str(self.nonce),
        })

    def get_hash(self):
        return sha256((str(self.data) + self.previous_hash + str(self.timestamp) + str(self.nonce)).encode()).hexdigest()
    
    def mine(self, difficulty: int):
        zeros = ''.join(['0' for zeros in range(0, difficulty)])
        while(self.get_hash()[0: difficulty] != zeros):
            self.nonce += 1
