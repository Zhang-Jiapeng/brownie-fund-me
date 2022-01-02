from scripts.helpful_script import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deloy import deploy_fund_me
from brownie import accounts,network, exceptions
import pytest

def test_can_fund_and_witdraw():
  account = get_account()
  fund_me = deploy_fund_me()
  entrance_fee = fund_me.getEntranceFee()
  tx1 = fund_me.fund({"from": account, "value": entrance_fee})
  tx1.wait(1)
  assert fund_me.addressToAmountFunded(account.address) == entrance_fee

  tx2 = fund_me.withdraw({"from": account})
  tx2.wait(1)
  assert fund_me.addressToAmountFunded(account.address) == 0

def test_owner_only_can_withdraw():
  if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
    pytest.skip("Only for local testting")
  account = get_account()
  fund_me = deploy_fund_me()
  bad_account = accounts.add()
  with pytest.raises(ValueError):
    fund_me.withdraw({"from": bad_account})
