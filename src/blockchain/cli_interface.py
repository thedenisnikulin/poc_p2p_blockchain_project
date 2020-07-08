import sys
import os
from typing import Tuple, Set
from PyInquirer import prompt
import socket
import pickle
# local
from Blockchain import Blockchain
from Transaction import Transaction


def use_blockchain(blockchain: Blockchain, current_address: Tuple[str, int], peers: Set[Tuple[str, int]]):

    questions = {
        'main': {
            'type': 'list',
            'name': 'main',
            'message': f'Balance: {blockchain.get_balance(current_address)}\nActions:',
            'choices': ['Get chain', 'New transaction', 'Mine block', 'Quit'],
        },
        'peers': {
            'type': 'list',
            'name': 'peers',
            'message': 'Whom to send?',
            'choices': [str(p) for p in peers]
        },
        'amount': {
            'type': 'input',
            'name': 'amount',
            'message': 'What amount would you like to send?'
        }
    }

    answer = prompt(questions['main'])
    # GET CHAIN
    if answer['main'] == 'Get chain':
        print(blockchain.__str__)
        input('\nPress [ Enter ] to continue')
    # NEW TRANSACTION
    elif answer['main'] == 'New transaction':
        try:
            answer = prompt(questions['peers'])
            recipient = answer['peers'].split(', ')
            recipient = recipient[0][2: -1], int(recipient[1][0: -1])
            answer = prompt(questions['amount'])
            t = Transaction(current_address, recipient, int(answer['amount']))
            blockchain.new_transaction(t)
        except IndexError:
            # This error raises when we get empty set
            print('No connected peers :(')
    # MINE BLOCK
    elif answer['main'] == 'Mine block':
        blockchain.add_block()
        clearconsole()
    # QUIT
    elif answer['main'] == 'Quit':
        sys.exit()


def clearconsole():
    """
    Clear the console.
    """
    if os.name == "posix":
        # Unix/Linux/MacOS/BSD/etc
        os.system('clear')
    elif os.name in ("nt", "dos", "ce"):
        # DOS/Windows
        os.system('CLS')



