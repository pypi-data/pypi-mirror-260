from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://eth1.lava.build/lava-referer-aabba18d-f17d-4a8d-b374-880be0eec03a/'))


def get_balance(account):
    balance = w3.from_wei(w3.eth.get_balance(account), "ether")
    return balance
