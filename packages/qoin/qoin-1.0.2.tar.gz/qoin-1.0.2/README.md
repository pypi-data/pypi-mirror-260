[![PyPI version](https://img.shields.io/pypi/v/qoin)](//pypi.org/project/qoin)

# Qoin
`qoin` is the analogue of `random` package implemented through gate-based quantum computing.

## Getting Started

### Prerequisites
- Python 3.9+

### Installation
`qoin` can be installed with the command :
```
pip install qoin
```
The default installation of `qoin` includes `numpy`, `qiskit`, and `qiskit_aer`.

## Usage
The docs/examples are a good way for understanding how the package works.
```
from qoin import QRNG
from qiskit_aer import AerSimulator


random_generator = QRNG(backend=AerSimulator())
random_generator.randint(5, 10)
```

## License
The package is released under the GPL Ver 3.0 license.
