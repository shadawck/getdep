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
            'pip'
            ]
    
def print_supported_pms():
    """ Print supported pms """
    supported_pms = get_supported_pms()
    print("Supported PMS are : ")
    for pms_name in supported_pms : 
        print("\t", pms_name)

def get_dependencies(pms_name, package):
    """Find Dependencies

    Get dependencies for a given package management system (PMS) and a given package

    Args : 
        pms_name (str): name of the pms sytem you want to use. See  get_supported_pms() for supported pms
        package (str): name of the package

    Returns: 
        completedProcess: The return value from run(), representing a process that has finished. https://docs.python.org/3/library/subprocess.html#subprocess.CompletedProcess
        We just need STDOUT for the other function. 
        "Captured stdout from the child process. A bytes sequence, or a string if run() was called with an encoding, errors, or text=True. None if stdout was not captured."

    """
    # Switch case for all pms supported : gem , apt, rpm , composer....
    if pms_name=="apt" or pms_name=='apt-get':
        commandToRun = ["sudo", "apt-rdepends", str(package)]

    elif pms_name=='npm' :
        commandToRun = ["sudo", "npm", "view", "--json", str(package), "dependencies"]
    
    elif pms_name=='gem' :
        base_url = "https://rubygems.org/api/v1/gems/"
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

    # Run command "commandToRun" for above pms
    p = subprocess.run(commandToRun, stdout=subprocess.PIPE,  encoding="ascii")
    return p

def print_dependencies(package, listDependencies):
    if listDependencies == [] :
        print("Ne dependencies found")
    else :
        print("The dependencies for <" + package + "> are :")
        for dep in listDependencies : 
            print("...", dep)