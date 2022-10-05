% extra-datascience-tools documentation master file, created by
% sphinx-quickstart on Fri Sep 30 10:21:32 2022.
% You can adapt this file completely to your liking, but it should at least
% contain the root `toctree` directive.



<!-- ```{include} ../../README.md
:relative-images:
``` -->
# Python package with extra tools for data science.
Welcome to `extra-datascience-tools`, a Python package which offers addition tools for data scientists. These tools include or will include e.g.:
- functions
- classes
- decorators
- graphs

which are useful and often used for most data science projects, so that you don't need to rewrite the same code over again or invent it yourself. Please be aware that this package was launched in oktober 2022 and thus the current amount of features might be limited, but the features that are present can be of great use.

Read the installation instructions in {doc}`installation`.
To see all functionalities consult the {doc}`autoapi/index`.

## Installation

To install extra-datasience-tools using PyPi

```console
pip install extra-datascience-tools
```

To install extra-datascience-tools without using PyPi
```console
git clone https://github.com/sTomerG/extra-datascience-tools.git
cd extra-data-science-tools
pip install .
```
If problems arise please upgrade pip:
```console
python3 -m pip install --upgrade pip
```

```{toctree}
:caption: 'Contents:'
:maxdepth: 4

installation
notebooks/tutorial
autoapi/index
about
```


## Indices and tables

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`
