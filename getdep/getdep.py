import json
from collections import OrderedDict
from getdep import utility

def get_apt_dependencies(package):
    """Get list of dependencies from apt command.
    
    Args:
        package (str): The package name for the apt package you want to install

    Return:
        list. A list of all dependencies found.

    """
    aptDependencies = []

    p = utility.get_dependencies("apt", package)
    # filter packages
    for word in p.stdout.split():
        if word.startswith("Depends:") or word.endswith(")") or word.startswith("("):
            continue
        aptDependencies.append(word)
    # remove double and the first element which is the "package" name
    aptDependencies = list(OrderedDict.fromkeys(aptDependencies[1:]))
    return aptDependencies

def get_pip_dependencies(package): 
    """Get list of dependencies from pip command.

    Args:
        package (str): The package name for the pip package you want to install.

    Return:
        list. A list of all dependencies found.

    """


    pipDependencies = []
    p = utility.get_dependencies("pip", package)
    
    try:    
        data = json.loads(p)['info']['requires_dist']
        for word in data : 
            pipDependencies.append(word.split()[0])
        
        # remove double
        pipDependencies = list(OrderedDict.fromkeys(pipDependencies))
            
    except TypeError:
        return [] # if data doesn't exist
    except json.decoder.JSONDecodeError:  
        print("Your package was not found on Pypi")
        return []


    return pipDependencies
        
def get_composer_dependencies(package): 
    """
    Get list of dependencies from composer command.
        
    Args:
        package (str): The package name for the composer package you want to install.
            Package need to be in composer format : <vendor>/<product>. Ex : laravel/install.

    Return:
        list. A list of all dependencies found.

    """
    composerDependencies = []
    try:
        p = utility.get_dependencies("composer", package)

        data = json.loads(p)["package"]["versions"]
        for x in data :
            # Get dev-master dependencies
            # dev_master = data["dev-master"]["require"]
            
            # get Latest stable version and break loop
            if x.startswith("v") :
                [composerDependencies.append(x) for x in data[x]["require"]]
                break

        return composerDependencies
        
    except UnboundLocalError:
        print("Your Package Management System : is not supported")
        utility.print_supported_pms()
        return []
    except KeyError:
        print("This package doesn't exist on packagist")
    except json.decoder.JSONDecodeError:
        # if data doesn't exist. At this moment composerDependencies = []
        return []

def get_gem_dependencies(package):
    """Get list of dependencies from gem command.
  
    Args:
        package (str): The package name for the gem package you want to install.

    Return:
        list. A list of all dependencies found.

    """

    gemDependencies = []
    try :
        p = utility.get_dependencies("gem", package)
        data = json.loads(p)["dependencies"]["runtime"]

        for word in data :
            gemDependencies.append(word["name"].strip())

        return gemDependencies

    except UnboundLocalError:
        print("Your Package Management System : is not supported")
        utility.print_supported_pms()
        return []
    except KeyError:
        print("This package doesn't exist on rubygem")
    except json.decoder.JSONDecodeError:
        # if data doesn't exist. At this moment composerDependencies = []
        return []

def get_npm_dependencies(package): 
    """Get list of dependencies from npm command.

    Args:
        package (str): The package name for the npm package you want to install.

    Return:
        list. A list of all dependencies found.

    """

    npmDependencies = []
    p = utility.get_dependencies("npm",package) # Json data
    try:    
        loaded_json = json.loads(p.stdout)
        for word in loaded_json:
        	npmDependencies.append(word)
            
    except json.decoder.JSONDecodeError:
        return []
    
    return npmDependencies

#def get_gem_dependencies_local(package): 
#    """Get list of dependencies from gem command.
#  
#    Args:
#        package (str): The package name for the gem package you want to install.
#
#    Return:
#        list. A list of all dependencies found.
#
#    """
#    gemDependencies = []
#    try:
#        p = utility.get_dependencies("gem", package)
#
#        motif = p.stdout.split("\n")
#
#        for word in motif[0:-1]: 
#            # remvove different Gem version
#            if word.startswith(package):
#                continue 
#            gemDependencies.append(word.split("--version")[0].strip())
#
#        # remove double
#        gemDependencies = list(OrderedDict.fromkeys(gemDependencies))
#
#        return gemDependencies
#        
#    except UnboundLocalError:
#        print("Your Package Management System : is not supported")
#        utility.print_supported_pms()
#        return []


