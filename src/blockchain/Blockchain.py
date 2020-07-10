from typing import List, Tuple, Set
# local
from networking import config
from blockchain.Block import Block
from blockchain.Transaction import Transaction


class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.difficulty = config.BLOCKCHAIN_DIFFICULTY

    def generate_genesis_block(self):
        # add genesis block
        if len(self.chain) == 0:
            print('Mining Block #0...')
            genesis = Block([], 'genesis')
            genesis.mine(self.difficulty)
            self.chain.append(genesis.serialized)

    def is_valid(self, chain_to_validate: List = None) -> bool:
        # if no chain in params, use self.chain. Else use chain in params.
        chain = self.chain if chain_to_validate is None else chain_to_validate
        for index in range(1, len(chain)):
            current_block = chain[index]
            previous_block = chain[index - 1]
            if current_block["previous_hash"] != previous_block["hash"]:
                return False
        return True

    def add_block(self, miner_address):
        # We reward those who mine with 1 coin, so we append a new transaction with this reward
        self.pending_transactions.append(Transaction('blockchain', miner_address, 1).serialized) # from blockchain, to miner, 1 coin
        # construct a new block
        new_block = Block(
            self.pending_transactions,
            self.chain[-1]['hash']
        )
        print(f'Mining block #{len(self.chain)}...')
        # mine it
        new_block.mine(self.difficulty)
        # and append to chain, cleaning the pending transaction ('cos we've already written them in the block)
        self.chain.append(new_block.serialized)
        self.pending_transactions = []

    def new_transaction(self, transaction: Transaction):
        self.pending_transactions.append(transaction.serialized)

    def replace_chain(self, new_chain: List):
        # if new chain is bigger, replace current with the new one
        if len(new_chain) > len(self.chain):
            self.chain = new_chain

    def get_balance(self, address):
        """
        Iterate through chain and find transactions where provided address appears.
        """
        balance = 0
        for block in self.chain:
            for t in block['transactions']:
                if t['recipient'] == address:
                    balance += t['amount']
                elif t['sender'] == address:
                    balance -= t['amount']
        return balance

    @property
    def __str__(self):
        return ''.join([(
                14 * '-' + f'Block #{self.chain.index(block)}' + '-' * 14 + '\n' +
                f'data: {block["transactions"]}\n' +
                f'hash: {block["hash"]}\n' +
                f'previous_hash: {block["previous_hash"]}\n' +
                f'timestamp: {block["timestamp"]}\n' +
                f'nonce: {block["nonce"]}\n'
        ) for block in self.chain])