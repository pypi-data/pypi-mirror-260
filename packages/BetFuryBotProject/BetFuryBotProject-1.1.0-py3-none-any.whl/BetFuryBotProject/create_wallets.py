import web3
from web3.auto import w3
from mnemonic import Mnemonic

def create_eth_wallet():
    mnemo = Mnemonic('english')
    words = mnemo.generate(strength=256)
    seed = mnemo.to_seed(words, passphrase="")
    entropy = mnemo.to_entropy(words)
    w3.eth.account.enable_unaudited_hdwallet_features()
    account = w3.eth.account.from_mnemonic(words)
    return (words)
