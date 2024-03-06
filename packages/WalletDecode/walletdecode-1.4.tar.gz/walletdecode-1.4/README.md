# WalletDecode
[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

![](https://img.shields.io/github/stars/pandao/editor.md.svg) ![](https://img.shields.io/github/forks/pandao/editor.md.svg) ![](https://img.shields.io/github/tag/pandao/editor.md.svg) ![](https://img.shields.io/github/release/pandao/editor.md.svg) ![](https://img.shields.io/github/issues/pandao/editor.md.svg) ![](https://img.shields.io/bower/v/editor.md.svg)

Simple Tools for decode crypto data, from extensions wallet, Metamask, Ronin, Brawe, TronLink(old), etc.


## Installation
Python requires [Python.org](https://www.python.org/) v3,7+ to run.
Install the dependencies and devDependencies and start the server.
```sh
python -m pip install pip
python -m pip install --upgrade pip
pip install pycryptodome
```
## Using Single Version
**Decrypt hash by one password:**

*default Metamask path in chrome*: 
###### C:\Users\root\AppData\Local\Google\Chrome\User Data\Default\Local Extension Settings\nkbihfbeogaeaoehlefnkodbefgpgknn
p.s payload search from log file, ******.log,

```python
from WalletDecode import extensionWalletDecrypt
pssw = "qwerty123"
payload = {"data": "M5YTg9f1PP62H........ATR/iKzdvhHdF", "iv": "6CD......Cg==", "salt": "TkHQ2......fxaSC/g="}
d1 = extensionWalletDecrypt()
obj = d1.decryptSingle(pssw, payload)
print(obj)
```
##Output:
```
[{'type': 'HD Key Tree', 'data': {'mnemonic': 'result slam keen employ smile capable crack network favorite equal limit orphan', 'numberOfAccounts': 1, 'hdPath': "m/44'/60'/0'/0"}}, {'type': 'Trezor Hardware', 'data': {'hdPath': "m/44'/60'/0'/0", 'accounts': [], 'page': 0, 'paths': {}, 'perPage': 5, 'unlockedAccount': 0}}, {'type': 'Ledger Hardware', 'data': {'hdPath': "m/44'/60'/0'", 'accounts': [], 'accountDetails': {}, 'implementFullBIP44': False}}]
```

## Using List Version
```python
from WalletDecode import extensionWalletDecrypt
pssw = ['qwerty123', 'qwerty321', 'qwerty1212', 'qwe211', 'qweqwerty0']
payload = {'data': 'M5YTg9f1PP62H........ATR/iKzdvhHdF', 'iv': '6CD......Cg==', 'salt': 'TkHQ2......fxaSC/g='}
d1 = extensionWalletDecrypt()
obj = d1.decryptList(pssw, payload)
print(obj)
```
Note: this app cant replace HashCat app, use only actual passwords.


## Best practice: virtual environments
In order to avoid problems with pip packages in different versions or packages that install under the same folder (i.e. `pycrypto` and `pycryptodome`) you can make use of a so called virtual environment. There, the installed pip packages can be managed for every single project individually.

To install a virtual environment and setup everything, use the following commands:

```Python
# install python3 and pip3
sudo apt update
sudo apt upgrade
sudo apt install python3
sudo apt install python3-pip

# install virtualenv
pip3 install virtualenv

# install and create a virtual environment in your target folder
mkdir target_folder
cd target_folder
python3 -m virtualenv .

# now activate your venv and install pycryptodome
source bin/activate
pip3 install pycryptodome

# check if everything worked: 
# start the interactive python console and import the Crypto module
# when there is no import error then it worked
python
>>> from Crypto.Cipher import AES
>>> exit()

# don't forget to deactivate your venv again
deactivate
```
For more information, see [docs.python-guide.org](http://docs.python-guide.org "docs.python-guide.org").



## License
MIT
>Decoder master project (c)