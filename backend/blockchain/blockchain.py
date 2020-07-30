from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction
from backend.config import MINING_REWARD_INPUT
from backend.wallet.wallet import Wallet
class Blockchain:
    def __init__(self):
       self.chain=[Block.genesis()]
    def add_block(self,data):
       last_block=self.chain[-1]
       self.chain.append(Block.mine_block(last_block,data))
    def __repr__(self):
        return f'Blockchain:{self.chain}'
    def replace_chain(self,chain):
       print(len(self.chain),len(chain))
       if len(chain)<=len(self.chain):
          raise Exception('Cannot replace.The incoming chain must be longer')
       try:
          Blockchain.is_valid_chain(chain)
       except Exception as e:
          raise Exception(f'Cannot replace.The incoming chain is invalid:{e}')
       self.chain=chain
    def to_json(self):
     return  list(map(lambda data:data.to_json(),self.chain))
    @staticmethod
    def from_json(chain_json):
       blockchain=Blockchain()
       blockchain.chain=list(map(lambda block_json:Block.from_json(block_json),chain_json))
       return blockchain

    @staticmethod
    def is_valid_chain(chain):
       if chain[0]!=Block.genesis():
         raise Exception('The genesis block must be valid')
       for i in range(1,len(chain)):
          block=chain[i]
          last_block=chain[i-1]
          Block.is_valid_block(last_block,block)
       Blockchain.is_valid_transaction_chain(chain)
    
    
    @staticmethod
    def is_valid_transaction_chain(chain):
       transaction_ids=set()
       for i in range(len(chain)):
          block=chain[i]
          has_mining_reward=False
          for transaction_json in block.data:
             transaction=Transaction.from_json(transaction_json)
             if transaction.id in transaction_ids:
                raise Exception(f'Transaction {transaction.id} is not unique')
             transaction_ids.add(transaction.id)
             if transaction.input==MINING_REWARD_INPUT:
                if has_mining_reward:
                   raise Exception('There can only be one mining reward per block'\
                   f'Check block with hash:{block.hash}'
                  )
                has_mining_reward=True
             
             else:
               historic_blockchain=Blockchain()
               historic_blockchain.chain=chain[0:i]
               historic_balance=Wallet.calculate_balance(historic_blockchain,transaction.input['address'])
               if historic_balance!=transaction.input['amount']:
                  raise Exception('Transaction {transaction.id} has an invalid input amount')
             Transaction.is_valid_transaction(transaction)
           
if(__name__=='__main__'):
  blockchain=Blockchain()
  blockchain.add_block('one')
  blockchain.add_block('two')
  print(blockchain)
