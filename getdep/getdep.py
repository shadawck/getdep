import json
from collections import OrderedDict
from getdep import utility
from pprint import pprint

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
        return []
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

# Use yarn for npm and yarn pms
def get_yarn_dependencies(package):
    yarnDependencies = []
    p = utility.get_dependencies("yarn", package)
    try :
        yarnDependencies = json.loads(p)["dependencies"]

    except UnboundLocalError:
        print("Your Package Management System : is not supported")
        utility.print_supported_pms()
        return []
    except KeyError:
        print("This package doesn't exist on yarn")
    except json.decoder.JSONDecodeError:
        # if data doesn't exist. At this moment composerDependencies = []
        return []
    
    return [word.split(':')[0] for word in yarnDependencies]

# Use for chocolatey and Nuget
def get_chocolatey_dependencies(package):
    """
    
    """
    package = package.lower()
    chocoDependencies = []
    p = utility.get_dependencies("choco", package)
    try :
        data = json.loads(p)
        chocoDependencies = []

        verCount = data["items"][0]["count"] - 1 
        items = data["items"][0]["items"][verCount]
        chocoDependencyGroups = items["catalogEntry"]["dependencyGroups"]

        for word in chocoDependencyGroups:
            chocoDependencies.append(word["targetFramework"])

    except UnboundLocalError:
        print("Your Package Management System : is not supported")
        utility.print_supported_pms()
        return []
    except KeyError:
        print("This package doesn't exist on nuget or chocolatey")
    except json.decoder.JSONDecodeError:
        # if data doesn't exist. At this moment composerDependencies = []
        return []
    
    return chocoDependencies
    
def get_pacman_dependencies(package):
    pass

def get_brew_dependencies(package):
    """Get list of dependencies from brew command.

    Args:
        package (str): The package name for the brew formulae you want to install.

    Return:
        list. A list of all dependencies found.

    """
    p = utility.get_dependencies("brew", package)

    try:
        # TODO : Search for other dependencies : uses_from_macos, build
        brewDependencies = json.loads(p)["dependencies"]
        
    except TypeError:
        return []
    except json.decoder.JSONDecodeError:  
        print("The package" ,package, "was not found on brew")
        return []
    
    return [word.split("@")[0] for word in brewDependencies]

def get_gem_dependencies_local(package): 
    """Get list of dependencies from gem command.
  
    Args:
        package (str): The package name for the gem package you want to install.

    Return:
        list. A list of all dependencies found.

    """
    gemDependencies = []
    try:
        p = utility.get_dependencies("gem", package)

        motif = p.stdout.split("\n")

        for word in motif[0:-1]: 
            # remvove different Gem version
            if word.startswith(package):
                continue 
            gemDependencies.append(word.split("--version")[0].strip())

        # remove double
        gemDependencies = list(OrderedDict.fromkeys(gemDependencies))

        return gemDependencies
        
    except UnboundLocalError:
        print("Your Package Management System : is not supported")
        utility.print_supported_pms()
        return []


# Used for RPM-based Linux distributions (fedora, CentOS). Basicaly any package using rpm and yum (soon DNF)
def get_yum_dependencies():
    pass

