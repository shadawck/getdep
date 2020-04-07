# GETDEP

Get dependencies for a given package management system and a given package. 

## Use

You can install ```getdep``` either via pip (PyPI) or from source.
To install using pip:
```bash
python3 -m pip install getdep
```
Or manually:
```
git clone https://github.com/remiflavien1/getdep 
cd getdep
./install.sh && setup.py
```

For ```apt``` dependencies you need to install ```apt-rdepends```:
```bash
sudo apt install apt-rdepends
```

## Use

```bash 
>>> from getdep import getdep
>>> getdep.get_pip_dependencies("requests")
['chardet', 'idna', 'urllib3', 'certifi', 'pyOpenSSL', 'cryptography', 'PySocks', 'win-inet-pton']
>>> getdep.get_apt_dependencies("nano")
['nano', 'libc6', 'libncursesw5', 'libtinfo5', 'libgcc1', 'gcc-8-base']

# Supported package management system
>>> from getdep import utility
>>> utility.print_supported_pms()
Supported PMS are : 
         apt        
         apt-get    
         composer   
         gem        
         npm        
         pip    
```




## Note 
You must have the package management system, which you are requesting, installed on your system.