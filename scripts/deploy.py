from brownie import FundMe, config, network, MockV3Aggregator
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from web3 import Web3
import os


def deploy_fund_me():
    account = get_account()
    # pass the price feed to our fundme contract

    # if we are network like rinkeby, use address else dploy mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
        w3 = Web3(
            Web3.HTTPProvider(
                "https://"
                + network.show_active()
                + ".infura.io/v3/"
                + os.getenv("WEB3_INFURA_PROJECT_ID")
            )
        )
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(price_feed_address, {"from": account})
    print(fund_me)
    print(
        f"Contract deployed to {fund_me.address}"
    )  # https://youtu.be/M576WGiDBdQ?t=19041 if you wanna publish your code. skipped here.
    return fund_me


def main():
    deploy_fund_me()
