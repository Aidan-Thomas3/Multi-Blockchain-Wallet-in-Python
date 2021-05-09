# Import dependencies
import subprocess
import json
import os
from dotenv import load_dotenv
from dotenv import dotenv_values
from constants import btc, eth, btctest
from pathlib import Path
from web3 import Web3
from web3 import middleware
from web3.middleware import geth_poa_middleware
from web3.auto.gethdev import w3
from eth_account import Account
from bit import *
from bit import wif_to_key
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI
from getpass import getpass

# Load and set environment variables
load_dotenv()
mnemonic = os.getenv("mnemonic")

# Web3
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
 
 
# Create a function called `derive_wallets`
def derive_wallets(coin = btc, mnemonic = mnemonic, depth = 3):
    command = 'php derive -g --mnemonic={mnemonic} --cols=path,address,privkey,pubkey --coin={coin} --numderive={depth} --format=json'
    p = subprocess.Popen(command, stdout = subprocess.PIPE, shell = True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)

# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {btctest: derive_wallets(coin = btctest), eth: derive_wallets(coin = eth)}

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin, priv_key):
    if coin == eth:
        return Account.privateKeyToAccount(priv_key)
    elif coin == btctest:
        return PrivateKeyTestnet(priv_key)
    

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin, account, recipient, amount):
    if coin == eth:
        gasEstimate = w3.eth.estimateGas(
            {"from": account, "to": recipient, "amount": value }
        )
        return{
            "from": account,
            "to": recipient,
            "value": amount,
            "gasPrice": w3.ethgasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account)
        }
    elif coin == btctest:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, btc)])


# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin, account, recipient, amount):
    tx = create_tx(coin, account, recipient, amount)
    if coin == eth:
        sign_tx = account.signTransaction(tx)
        return w3.eth.sendRawTransaction(sign_tx.rawTransaction)
    elif coin == btctest:
        btctest_tx = create_tx(coin, account, recipient, amount)
        sign_tx = account.sign_transaction(tx)
    return NetworkAPI.broadcast_tx_testnet(sign_tx)

