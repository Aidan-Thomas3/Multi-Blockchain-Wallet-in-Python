# Insturctions To Begin
`hd-wallet-derive` that supports not only BIP32, BIP39, and BIP44, but
also supports non-standard derivation paths for the most popular wallets out there today! However, you need to integrate
the script into your backend with your dear old friend, Python.
Once you've integrated this "universal" wallet, you can begin to manage billions of addresses across 300+ coins, giving
you a serious edge against the competition.

## Installions
### Needed Dependencies
- PHP must be installed on operating system (any version, 5 or 7). No need to know any PHP

- Clone the [`hd-wallet-derive`](https://github.com/dan-da/hd-wallet-derive) tool.

- [`bit`](https://ofek.github.io/bit/) Python Bitcoin library.

- [`web3.py`](https://github.com/ethereum/web3.py) Python Ethereum library.

### Installing hd-wallet-derive
open your git bash and run the following commands to clone the hd-wallet-derive & install.
`git clone https://github.com/dan-da/hd-wallet-derive`
`cd hd-wallet-derive`
`curl https://getcomposer.org/installer -o installer.php`
`php installer.php`
`php composer.phar install`

### create a repository
creating a repository named wallet and copying the hd-wallet-derive folder to it.
- opening your gitbash as administrator and running this code before changing directories.
`export MSYS=winsymlinks:nativestrict`
- once that has ran enter this command next to create a symlink called derive.
`ln -s hd-wallet-derive/hd-wallet-derive.php derive`
- this will allow us to call ./derive instead of 
`./hd-wallet-derive/hd-wallet-derive.php.exe.`

### python scripts
create a wallet.py file in this repository as well the organization should look like this.
![directory-tree](Images/tree.png)
- also create a file named constants.py with the following:
    - BTC ='btc'
    - ETH = 'eth'
    -BTCTEST = 'btc-test'
- importing tall constants into the wallet.py later.

### Retrieving a mnemonic phrase 
generate a new 12 word mnemonic using hd-wallet-deriveor using this [website](https://iancoleman.io/bip39/).
- using an environment variable to sotre the new mnemonic phrase and calling it into the wallet.py file.

### Deriving wallet keys
- Use the `subprocess` library to call the `./derive` script from Python. Make sure to properly wait for the process.
- The following flags must be passed into the shell command as variables:
  - Mnemonic (`--mnemonic`) must be set from an environment variable, or default to a test mnemonic
  - Coin (`--coin`)
  - Numderive (`--numderive`) to set number of child keys generated
- Set the `--format=json` flag, then parse the output into a JSON object using `json.loads(output)`

- Wrap all of this into one function, called `derive_wallets`

- Create an object called `coins` that derives `ETH` and `BTCTEST` wallets with this function.

### Linking Transactions Signing Libraries
- Use `bit` and `web3.py` to leverage the keys stored in the `coins` object by creating three more functions:

  1) `priv_key_to_account`: This function will convert the `privkey` string in a child key to an account object that `bit` or `web3.py` can use to transact. It needs the following parameters:
      - `coin` -- the coin type (defined in `constants.py`).
      - `priv_key` -- the `privkey` string will be passed through here.

   check the coin type, then return one of the following functions based on the library:

      - For `ETH`, return `Account.privateKeyToAccount(priv_key)`
      - For `BTCTEST`, return `PrivateKeyTestnet(priv_key)`

  2) `create_tx`: This function will create the raw, unsigned transaction that contains all metadata needed to transact. This function needs the following parameters:

      - `coin` -- the coin type (defined in `constants.py`).
      - `account` -- the account object from `priv_key_to_account`.
      - `to` -- the recipient address.
      - `amount` -- the amount of the coin to send.

    check the coin type, then return one of the following functions based on the library:

      - For `ETH`, return an object containing `to`, `from`, `value`, `gas`, `gasPrice`, `nonce`, and `chainID`.
        Make sure to calculate all of these values properly using `web3.py`!
      - For `BTCTEST`, return `PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])`

  3) `send_tx`: This function will call `create_tx`, sign the transaction, then send it to the designated network. it needs the following parameters:

    - `coin` -- the coin type (defined in `constants.py`).
    - `account` -- the account object from `priv_key_to_account`.
    - `to` -- the recipient address.
    - `amount` -- the amount of the coin to send.

  these are the exact same parameters as `create_tx`. `send_tx` will call `create_tx`. To check the coin, then create a `raw_tx` object by calling `create_tx`. Then sign the `raw_tx` using `bit` or `web3.py`(hint: the account objects have a sign transaction function within).

  - Once you've signed the transaction, you will need to send it to the designated blockchain network.

    - For `ETH`, return `w3.eth.sendRawTransaction(signed.rawTransaction)`
    - For `BTCTEST`, return `NetworkAPI.broadcast_tx_testnet(signed)`

### Executing Transactions
- 

