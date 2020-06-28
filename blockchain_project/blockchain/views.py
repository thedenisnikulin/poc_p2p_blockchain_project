from django.shortcuts import render
from django.http import request, HttpRequest
from .services.Blockchain import Blockchain


blockchain = Blockchain()

def get_chain(request: HttpRequest):
    return render (request, 'index.html', {'chain': ['index: {}, hash: {}'.format(blockchain.chain.index((b)), b.get_hash()) for b in blockchain.chain]})

def mine_block(request: HttpRequest):
    pass

def new_transaction(request: HttpRequest):
    pass
