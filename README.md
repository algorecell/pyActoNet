# pyActoNet

Implementation of abduction-based control of fixed points of Boolean networks
([Biane et al, 2019](https://doi.org/10.1109/TCBB.2018.2889102)),
using Answer-Set Programming

The control predictions can be processed using the [algorecell_types](https://github.com/algorecell/algorecell_types) library, which eases the
display and comparison with other control methods.

## Installation

<!--
### CoLoMoTo Notebook environment

`pyActoNet` is distributed as part of the [CoLoMoTo docker](http://colomoto.org/notebook).

-->

### Using conda
```
conda install -c colomoto pyactonet
```

### Using pip

#### Extra requirements
* [clingo](https://github.com/potassco/clingo) and its Python module

```
pip install actonet
```

## Documentation

Documentation is available at https://pyactonet.readthedocs.io.

Examples can be found at:
* https://nbviewer.jupyter.org/github/algorecell/pyactonet/tree/master/examples/

## Authors

* Célia Biane
* Jacques Nicolas
* [Loïc Paulevé](https://github.com/pauleve)
