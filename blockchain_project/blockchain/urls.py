from django.urls import path
from .views import get_chain, mine_block, new_transaction

urlpatterns = [
    path('chain/get', get_chain),
    path('chain/mine-block', mine_block),
    path('transactions/new', new_transaction)
]