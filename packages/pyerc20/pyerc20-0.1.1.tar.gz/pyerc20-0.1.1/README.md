pyerc20 is a python implementation of the ERC20 standard.

## Getting Started
```
pip install pyerc20
```

## Usage

```python
from web3 import Web3
from pyerc20 import ERC20
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
erc20 = ERC20(w3,'0x...')
```

