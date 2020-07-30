import os
import random
import requests
from flask import Flask,jsonify,request
from flask_cors import CORS,cross_origin
from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool

app=Flask(__name__)
CORS(app,resources={r'/*':{'origins':'http://localhost:3000'}})
blockchain=Blockchain()
wallet=Wallet(blockchain)
transactionpool=TransactionPool()
pubsub=PubSub(blockchain,transactionpool)

@app.route('/')
def route_default():
    return 'Welcome to the blockchain'



@app.route('/blockchain')
def route_blockchain():
   return jsonify(blockchain.to_json())



@app.route('/blockchain/range')
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def route_blockchain_range():
    start=int(request.args.get('start'))
    end=int(request.args.get('end'))
    return jsonify(blockchain.to_json()[::-1][start:end])




@app.route('/blockchain/length')
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def route_blockchain_length():
    return jsonify(len(blockchain.chain))



@app.route('/blockchain/mine')
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def route_blockchain_mine():
    transaction_data=transactionpool.transaction_data()
    transaction_data.append(Transaction.reward_transaction(wallet).to_json())
    blockchain.add_block(transaction_data)
    block=blockchain.chain[-1]
    
    pubsub.broadcast_block(block)
    transactionpool.clear_blockchain_transactions(blockchain)
    return jsonify(block.to_json())


ROOT_PORT=5000



@app.route('/wallet/transact',methods=['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def route_wallet_transact():
    
    transaction_data=request.get_json()
    transaction=transactionpool.existing_transaction(wallet.address)
    if transaction:
        transaction.update(wallet,transaction_data['recipient'],transaction_data['amount'])
    else:
        transaction=Transaction(wallet,transaction_data['recipient'],transaction_data['amount'])
        print(f'transaction.to_json():{transaction.to_json()}')
    pubsub.broadcast_transaction(transaction)
    return jsonify(transaction.to_json())



@app.route('/wallet/info')
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def route_wallet_info():
    return jsonify({'address':wallet.address,'balance':wallet.balance})

@app.route('/known-addresses')
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def route_known_addresses():
    known_addresses=set();
    for block in blockchain.chain:
        for transaction in block.data:
            
            known_addresses.update(transaction['output'].keys())
    return jsonify(list(known_addresses))

@app.route('/transactions')
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def route_transactions():
    return jsonify(transactionpool.transaction_data())

PORT=ROOT_PORT

if os.environ.get('PEER')=='True':
    PORT=random.randint(5001,6000)
    result=requests.get(f'http://localhost:{ROOT_PORT}/blockchain')
    result_blockchain=Blockchain.from_json(result.json())
    try:
      blockchain.replace_chain(result_blockchain.chain)
      print('\n successfully synchronised the local chain')
    except Exception as e:
        print(f' \n Error synchronising:{e}')
if os.environ.get('SEED_DATA')=='True':
    for i in range(10):
        blockchain.add_block([
            Transaction(Wallet(),Wallet().address,random.randint(2,50)).to_json(),
            Transaction(Wallet(),Wallet().address,random.randint(2,50)).to_json()

        ])
    for i in range(3):
        transactionpool.set_transaction(Transaction(Wallet(),Wallet().address,random.randint(2,50)))
print(blockchain)         
app.run(port=PORT)
