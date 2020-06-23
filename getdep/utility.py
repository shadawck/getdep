# !/usr/bin/env python3

import subprocess
import shlex
import requests

def get_supported_pms():
    """List of supported and implemented pms. 
    
    More to come in the future (rpm, pkg, c/c++, cargo ...)
    
    """
    return ['apt', 
            'apt-get', 
            'composer',
            'gem',
            'npm',
            'yarn',
            'brew',
            'pip',
            'choco',
            'dotnet',
            'yum,dnf,rpm'
            ]
    
def print_supported_pms():
    """ Print supported pms """
    supported_pms = get_supported_pms()
    print("Supported PMS are : ")
    for pms_name in supported_pms : 
        print("\t", pms_name)

def print_dependencies(package, listDependencies):
    if listDependencies == [] :
        print("No dependencies found")
    else :
        print("The dependencies for <" ,package,"> are :")
        for dep in listDependencies : 
            print("...", dep)

def get_dependencies(pms_name, package):
    """

    Get dependencies for a given package management system (PMS) and a given package.

    Args : 
        pms_name (str): name of the pms sytem you want to use. See  get_supported_pms() for supported pms.   
        
        package (str): name of the package.   

    Returns: 
        subprocess.CompletedProcess or content of the `request.get` in unicode: The return value from `subprocess.run`, representing a process that has finished. Look at the documentation `here <https://docs.python.org/3/library/subprocess.html#subprocess.CompletedProcess>`_
        We just need `subprocess.stdout` for `getdep` module functions.

    TODO : 
        Separate into two functions to have a uniform return type.

    """
    # Switch case for all pms supported : gem , apt, rpm , composer....
    if pms_name=="apt" or pms_name=='apt-get':
        commandToRun = ["sudo", "apt-rdepends", str(package)]
        p = subprocess.run(commandToRun, stdout=subprocess.PIPE,  encoding="ascii")
        return p
    elif pms_name=="rpm" or pms_name=='yum' or pms_name=="dnf":
        commandToRun = ["sudo", "yum", "-q", "deplist", str(package)]
        p = subprocess.run(commandToRun, stdout=subprocess.PIPE,  encoding="ascii")
        return p
    
    elif pms_name=='yarn' or pms_name == 'npm':
        base_url = "https://cdn.jsdelivr.net/npm/"
        url = base_url + package + "/package.json"
        return requests.get(url,stream=True)
    
    elif pms_name=='gem' :
        base_url = "https://rubygems.org/api/v1/gems/"
        url = base_url + package + ".json" 
        return requests.get(url,stream=True).text
        
    elif pms_name=='brew':
        base_url = "https://formulae.brew.sh/api/formula/"
        url = base_url + package + ".json" 
        return requests.get(url,stream=True).text
        
    elif pms_name == 'composer' :  
        base_url = "https://repo.packagist.org/packages/"
        # Make api request to packagist # Ex : GET https://repo.packagist.org/packages/paragonie/random-lib.json
        url = base_url + package + ".json" 
        return requests.get(url, stream=True).text 

    elif pms_name == 'pip': 
        base_url = "https://pypi.org/pypi/"
        url = base_url + package + "/json" 
        return requests.get(url,stream=True).text
    # used for nuget and chocolatey    
    elif pms_name == 'choco' or pms_name == 'dotnet':
        base_url = "https://api.nuget.org/v3/registration3/"
        url = base_url + package + "/index.json" 
        return requests.get(url,stream=True).text
