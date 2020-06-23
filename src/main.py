import redis
import json
from Blockchain import Blockchain

def run():
    storage = redis.Redis(host="localhost", port=6379, db=0)
    blockchain = Blockchain()
    blockchain.add_block({'amount': 1})
    blockchain.add_block({'amount': 2})
    blockchain.add_block({'amount': 3})
    blockchain.add_block({'amount': 4})

    for block in blockchain.chain:
        storage.set('block_{}'.format(block.index), block.serialize())
        print(storage.get('block_{}'.format(block.index)).decode())



if __name__ == "__main__":
    run()