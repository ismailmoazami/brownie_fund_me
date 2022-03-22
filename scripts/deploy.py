from brownie import FundMe, config, accounts, network, MockV3Aggregator
from scripts.helper_functions import get_account, get_mock, LOCAL_BLOCKCHAINS


def deploy_fund_me():
    account = get_account()

    if network.show_active() not in LOCAL_BLOCKCHAINS:
        price_feed_address = config['networks'][network.show_active()]['eth_usd_price_feed']
    else: 
        get_mock()
        price_feed_address = MockV3Aggregator[-1].address
    
    fund_me = FundMe.deploy(price_feed_address, {"from": account}, 
    publish_source=config['networks'][network.show_active()].get('verify'))
    print(f"Contract deployed to {fund_me.address}")
    return fund_me
    
def main(): 
    deploy_fund_me()