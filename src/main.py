import json
from Blockchain import Blockchain
from Transaction import Transaction
from Block import Block

def run():
    blockchain = Blockchain()
    blockchain.new_transaction(Transaction('from', 'to', 3))
    blockchain.add_block()
    print(blockchain.__str__)


if __name__ == "__main__":
    run()