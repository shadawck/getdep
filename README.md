# GETDEP

[![codecov](https://codecov.io/gh/remiflavien1/getdep/branch/master/graph/badge.svg)](https://codecov.io/gh/remiflavien1/getdep)  [![PyPI version](https://badge.fury.io/py/getdep.svg)](https://badge.fury.io/py/getdep) [![Requirements Status](https://requires.io/github/remiflavien1/getdep/requirements.svg?branch=master)](https://requires.io/github/remiflavien1/getdep/requirements/?branch=master) [![Documentation Status](https://readthedocs.org/projects/mitrecve/badge/?version=latest)](https://getdep.readthedocs.io/en/latest/?badge=latest)

Get dependencies for a given package management system and a given package. 

## Install

You can install ```getdep``` either via pip (PyPI) or from source.
To install using pip:
```bash
python3 -m pip install getdep
```
Or manually:
```
git clone https://github.com/remiflavien1/getdep 
cd getdep   
./install.sh   
python3 setup.py install   
```

For ```apt``` dependencies you need to install ```apt-rdepends```:
```bash
sudo apt install apt-rdepends
```

## Use

All the documentation is on [Readthedocs](https://mitrecve.readthedocs.io/)

## Note 
You must have the apt, rpm, and yum installed on your system if you want to get one of theirs packages dependencies.