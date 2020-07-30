from backend.wallet.transaction_pool import TransactionPool
from backend.wallet.transaction import Transaction
from backend.wallet.wallet  import Wallet
from backend.blockchain.blockchain import Blockchain
def test_set_transaction():
    transaction_pool=TransactionPool()
    transaction=Transaction(Wallet(),'recipient',40)
    transaction_pool.set_transaction(transaction)
    assert transaction_pool.transaction_map[transaction.id]==transaction
def test_clear_blockchain_transactions():
    transactionpool=TransactionPool()
    transaction_1=Transaction(Wallet(),'recipient',40)
    transaction_2=Transaction(Wallet(),'recipient',41)
    transactionpool.set_transaction(transaction_1)
    transactionpool.set_transaction(transaction_2)
    blockchain=Blockchain()
    blockchain.add_block([transaction_1.to_json(),transaction_2.to_json()])
    assert transaction_1.id in transactionpool.transaction_map
    assert transaction_2.id in transactionpool.transaction_map
    transactionpool.clear_blockchain_transactions(blockchain)
    assert not transaction_1.id in transactionpool.transaction_map
    assert not transaction_2.id in transactionpool.transaction_map