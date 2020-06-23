from hashlib import sha256
import json
import datetime

class Block():
    def __init__(self, index: int, data: dict, previous_hash: str):
        self.index = index
        self.data = data
        self.previous_hash = previous_hash
        self.timestamp = datetime.date.today()
        self.nonce = 0
    
    def serialize(self) -> str:
        return(json.dumps({
            'index': str(self.index),
            'data': self.data,
            'hash': self.get_hash(),
            'previous_hash': self.previous_hash,
            'timestamp': str(self.timestamp),
            'nonce': str(self.nonce),
        }))

    def get_hash(self):
        return(sha256((str(self.index)+ self.previous_hash + str(self.data) + str(self.timestamp) + str(self.nonce)).encode()).hexdigest())
    
    def mine(self, difficulty: int):
        number_of_zeros = ''.join(['0' for number_of_zeros in range(0, difficulty)])
        while(self.get_hash()[0: difficulty] != number_of_zeros):
            self.nonce += 1

