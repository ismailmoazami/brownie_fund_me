from brownie import accounts, network, config, MockV3Aggregator
from web3 import Web3

LOCAL_BLOCKCHAINS = ['development', 'ganache-local']


DECIMALS = 8
STARTING_PRICE = 200000000000

def get_account():
    if network.show_active() in LOCAL_BLOCKCHAINS:
        return accounts[0] 
    else: 
        return accounts.add(config['wallet']['from_key']) 

def get_mock():
    print("Deploying mock...")
    if len(MockV3Aggregator)<= 0:
         mock_contract = MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
         print("Mock deployed!")