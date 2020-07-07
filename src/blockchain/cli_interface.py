import sys
import os
from typing import Tuple, Set
from PyInquirer import prompt
import socket
# local
from Blockchain import Blockchain
from Transaction import Transaction


def use_blockchain(sock: socket.socket, chain: Blockchain, peers: Set[Tuple[str, int]]):
    questions = {
        'main': {
            'type': 'list',
            'name': 'main',
            'message': 'Actions',
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
    current_address = sock.getsockname()
    send = lambda data_to_send: sock.send(bytes(data_to_send, 'utf-8'))

    while 1: # TODO: make sending no-str data great again
        answer = prompt(questions['main'])
        if answer['main'] == 'Get chain':
            print(chain.__str__)
            input('\nPress [ Enter ] to continue')
        elif answer['main'] == 'New transaction':
            try:
                answer = prompt(questions['peers'])
                recipient = answer['peers'].split(', ')
                recipient = recipient[0][2: -1], int(recipient[1][0: -1])
                answer = prompt(questions['amount'])
                t = Transaction(current_address, recipient, int(answer['amount']))
                chain.new_transaction(t)
                send(chain)
            except IndexError:
                # This error raises when we get empty set
                print('No peers connected peers :(')
        elif answer['main'] == 'Mine block':
            chain.add_block()
            send(chain)
            clearconsole()
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



