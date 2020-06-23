from typing import List
from Block import Block

class Blockchain():
    def __init__(self):
        self.chain: List[Block] = [Block(0, {}, '')]
        self.difficulty = 4
    
    def is_valid(self):
        for index in range(1, len(self.chain)):
            current_block = self.chain[index]
            previous_block = self.chain[index - 1]

            if (current_block.hash != current_block.calculcate_hash()):
                return False
            if (current_block.previous_hash != previous_block.hash):
                return False
            return True

    def add_block(self, data: dict):
        new_block = Block(len(self.chain), data, self.chain[-1].get_hash())
        new_block.mine(self.difficulty)
        self.chain.append(new_block)
    
    def print(self):
        [print(('-----------------------\n' +
                'index: {}\n' +
                'data: {}\n' +
                'previous_hash: {}\n' + 
                'timestamp: {}\n' + 
                'nonce: {}').format(i.index, i.data, i.previous_hash, i.timestamp, i.nonce)) for i in self.chain]
