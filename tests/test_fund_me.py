from brownie import FundMe, network, exceptions, accounts
from scripts.helper_functions import get_account, LOCAL_BLOCKCHAINS
from scripts.deploy import deploy_fund_me
import pytest 

def test_can_fund_and_withdraw():
    account = get_account()
    fund_me_contract = deploy_fund_me()
    entrance_fee = fund_me_contract.getEntranceFee()
    tx = fund_me_contract.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    expected = entrance_fee
    assert expected == fund_me_contract.addressToAmountFunded(account.address)
    tx2 = fund_me_contract.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me_contract.addressToAmountFunded(account.address) == 0

def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAINS:
        pytest.skip("Only local networks!")
    bad_actor = accounts.add()
    fund_me = deploy_fund_me()
    
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
