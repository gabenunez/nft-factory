#TODO Payments module to handle payments for services

from eth_account.messages import defunct_hash_message
from hexbytes import HexBytes
import web3
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv('../')

infura_project_id = os.environ.get('infura_id')

w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{infura_project_id}'))
token_abi = """
[{
  "constant": true,
  "inputs": [
    {
      "name": "_owner",
      "type": "address"
    }
  ],
  "name": "balanceOf",
  "outputs": [
    {
      "name": "balance",
      "type": "uint256"
    }
  ],
  "payable": false,
  "type": "function"
}]
"""

cbears = '0xE020adb9e242702F1284440CF80dF635E9a458c3'

token_instance = w3.eth.contract(address=cbears,abi=token_abi)

def process_signed_transaction(signed_tx):
    message_hash = defunct_hash_message(text="Validate Bear Ownership")
    address = web3.Account.recoverHash(message_hash,signature=signed_tx)
    balance = token_instance.functions.balanceOf(address).call()
    return balance >= 1



# nftfactory_abi = """
# [
#     {
#         "inputs": [],
#         "stateMutability": "nonpayable",
#         "type": "constructor"
#     },
#     {
#         "anonymous": false,
#         "inputs": [
#             {
#                 "indexed": false,
#                 "internalType": "address",
#                 "name": "creator",
#                 "type": "address"
#             },
#             {
#                 "indexed": false,
#                 "internalType": "string",
#                 "name": "name",
#                 "type": "string"
#             },
#             {
#                 "indexed": false,
#                 "internalType": "string",
#                 "name": "symbol",
#                 "type": "string"
#             }
#         ],
#         "name": "ContractCreation",
#         "type": "event"
#     },
#     {
#         "anonymous": false,
#         "inputs": [
#             {
#                 "indexed": false,
#                 "internalType": "address",
#                 "name": "payee",
#                 "type": "address"
#             },
#             {
#                 "indexed": false,
#                 "internalType": "uint256",
#                 "name": "value",
#                 "type": "uint256"
#             }
#         ],
#         "name": "Purchased",
#         "type": "event"
#     },
#     {
#         "inputs": [],
#         "name": "buy",
#         "outputs": [],
#         "stateMutability": "payable",
#         "type": "function"
#     },
#     {
#         "inputs": [],
#         "name": "name",
#         "outputs": [
#             {
#                 "internalType": "string",
#                 "name": "",
#                 "type": "string"
#             }
#         ],
#         "stateMutability": "view",
#         "type": "function"
#     },
#     {
#         "inputs": [
#             {
#                 "internalType": "uint256",
#                 "name": "price",
#                 "type": "uint256"
#             }
#         ],
#         "name": "setPrice",
#         "outputs": [],
#         "stateMutability": "nonpayable",
#         "type": "function"
#     },
#     {
#         "inputs": [],
#         "name": "symbol",
#         "outputs": [
#             {
#                 "internalType": "string",
#                 "name": "",
#                 "type": "string"
#             }
#         ],
#         "stateMutability": "view",
#         "type": "function"
#     },
#     {
#         "inputs": [],
#         "name": "withdraw",
#         "outputs": [],
#         "stateMutability": "nonpayable",
#         "type": "function"
#     }
# ]

# """

# nft_factory_instance = w3.eth.contract(address='0xd143b54687299c08b83a40dfe1317e27a793ab7f',abi=nftfactory_abi)