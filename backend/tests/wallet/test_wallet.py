from backend.wallet.wallet import Wallet
from backend.blockchain.blockchain import Blockchain
from backend.wallet.transaction import Transaction
def test_verify_valid_signature():
    data={'foo':'test-data'}
    wallet=Wallet()
    signature=wallet.sign(data)
    assert Wallet.verify(wallet.public_key,data,signature)
def test_verify_invalid_signature():
    data={'foo':'test_data'}
    wallet=Wallet()
    signature=wallet.sign(data)
    assert not Wallet.verify(Wallet().public_key,data,signature)
def test_calculate_balance():
    blockchain=Blockchain()
    wallet=Wallet()
    assert Wallet.calculate_balance(blockchain,wallet.address)==wallet.balance
    transaction=Transaction(wallet,'recipient',30)
    blockchain.add_block([transaction.to_json()])
    assert Wallet.calculate_balance(blockchain,wallet.address)==wallet.balance-30
    received_amount_1=25
    recieved_transaction_1=Transaction(Wallet(),
    wallet.address,received_amount_1)
    received_amount_2=25
    recieved_transaction_2=Transaction(Wallet(),
    wallet.address,received_amount_2)
    blockchain.add_block([recieved_transaction_1.to_json(),recieved_transaction_2.to_json()])
    assert Wallet.calculate_balance(blockchain,wallet.address)==wallet.balance-30+received_amount_1+received_amount_2
    