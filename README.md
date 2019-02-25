[![Build Status](https://travis-ci.org/DavidMStraub/parameterscan.svg?branch=master)](https://travis-ci.org/DavidMStraub/parameterscan) [![Coverage Status](https://coveralls.io/repos/github/DavidMStraub/parameterscan/badge.svg?branch=master)](https://coveralls.io/github/DavidMStraub/parameterscan?branch=master)

# parameterscan

A simple Python package for doing parameter scans.

## Installation

Clone the repository or download and extract a source archive. Then change into the base directory an execute
```bash
python3 -m pip install . --user
```
possibly adding the `-e` flag for a development installation.


## Example

Set up an SQLite database to store the scan data:

```python
from parameterscan import ScanStoreSQL
store = ScanStoreSQL('my scan', datadir='.')
```

Define functions for generation of random parameters and quantities to compute as a function of parameters:

```python
import numpy as np

def random_parameters():
    return {'x': np.random.rand(), 'Y': np.random.rand(3, 3)}

def observables(par):
    return {'obs1': 3 * par['x'], 'obs2': np.linalg.det(par['Y'])}
```

Set up and start a random parameter scan:

```python
from parameterscan import RandomScan
scan = RandomScan(store,
                  parfunc=random_parameters,
                  funcdic={'observables': observables})
scan.run(batchsize=10, batches=100)
```

Display the results as `pandas` data frame:

```python
store.get('parameters')
store.get('observables')
```
