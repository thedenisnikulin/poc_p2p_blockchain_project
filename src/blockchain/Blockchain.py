from typing import List, Tuple, Set
# local
from blockchain.Block import Block
from blockchain.Transaction import Transaction


class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.difficulty = 4

    def generate_genesis_block(self):
        # add genesis block
        if len(self.chain) == 0:
            print('Mining Block #0...')
            genesis = Block([], 'genesis')
            genesis.mine(self.difficulty)
            self.chain.append(genesis)
        else:
            raise Exception('Tried to generate genesis block when it is not necessary')

    def is_valid(self, chain_to_validate: List[Block] = None):
        chain = self.chain if chain_to_validate is None else chain_to_validate
        for index in range(1, len(chain)):
            current_block = chain[index]
            previous_block = chain[index - 1]
            if current_block.previous_hash != previous_block.get_hash():
                return False
        return True

    def add_block(self):
        new_block = Block(
            [t.serialized for t in self.pending_transactions],
            self.chain[-1].get_hash()
        )
        print(f'Mining block #{len(self.chain)}...')
        new_block.mine(self.difficulty)
        self.chain.append(new_block)
        self.pending_transactions = []

    def new_transaction(self, transaction: Transaction):
        self.pending_transactions.append(transaction)

    def replace_chain(self, new_chain: List[Block]):
        is_valid = self.is_valid(new_chain)
        if is_valid and len(new_chain) > len(self.chain):
            return
        else:
            raise Exception('Cannot replace chain: new chain is not valid or is less than current.')

    @property
    def __str__(self):
        return ''.join([(
            14 * '-' + f'Block #{self.chain.index(block)}' + '-' * 14 + '\n' +
             f'data: {block.data}\n' +
             f'hash: {block.get_hash()}\n' +
             f'previous_hash: {block.previous_hash}\n' +
             f'timestamp: {block.timestamp}\n' +
             f'nonce: {block.nonce}\n'
        ) for block in self.chain])
