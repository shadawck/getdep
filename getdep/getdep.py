import json
from collections import OrderedDict
from getdep import utility
from pprint import pprint

def get_apt_dependencies(package):
    """Get list of dependencies from apt command.

    You need to have apt and apt-rdepends installed on your system. 
    
    Args:
        package (str): The package name for the apt package you want to install

    Return:
        list. A list of all dependencies found.

    Exemple:

    .. code-block:: python

        >>> from getdep import getdep 
        >>> getdep.get_apt_dependencies("nano")
        ['libc6', 'libncursesw6', 'libtinfo6', 'libcrypt1', 'libgcc-s1', 'gcc-10-base']


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
    """Get list of dependencies from pip package.

    Args:
        package (str): The package name for the pip package you want to install.

    Return:
        list. A list of all dependencies found.

    Exemple:

    .. code-block:: python

        >>> from getdep import getdep 
        >>> getdep.get_pip_dependencies("tensorflow")
        ['absl-py', 'astunparse', 'gast', 'google-pasta', 'h5py', 'keras-preprocessing', 'numpy', 'opt-einsum', 'protobuf', 'tensorboard', 
        'tensorflow-estimator', 'termcolor', 'wrapt', 'six', 'grpcio', 'wheel', 'mock', 'functools32', 'scipy', 'backports.weakref', 'enum34']

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
    Get list of dependencies from composer package.
        
    Args:
        package (str): The package name for the composer package you want to install.
            Package need to be in composer format : <vendor>/<product>. Ex : laravel/install.

    Return:
        list. A list of all dependencies found.

    Exemples:

    .. code-block:: python

        >>> from getdep import getdep 
        >>> getdep.get_composer_dependencies("twig/twig")
        ['php', 'symfony/polyfill-mbstring', 'symfony/polyfill-ctype']

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
        # if data doesn't exist. At this moment composerDependencies = []
        return []
    except json.decoder.JSONDecodeError:
        print("This package doesn't exist on packagist")
        return []

def get_gem_dependencies(package):
    """Get list of dependencies for gem package.
  
    Args:
        package (str): The package name for the gem package you want to install.

    Return:
        list. A list of all dependencies found.

    Exemple:

    .. code-block:: python
        
        >>> from getdep import getdep 
        >>> getdep.get_gem_dependencies("rail")
        ['actioncable', 'actionmailbox', 'actionmailer', 'actionpack', 'actiontext', 'actionview', 'activejob', 'activemodel', 'activerecord', 'activestorage', 
        'activesupport', 'bundler', 'railties', 'sprockets-rails']

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
        return []
    except json.decoder.JSONDecodeError:
        print("This package doesn't exist on rubygem")

# Use yarn for npm and yarn pms
def get_npm_dependencies(package):
    """Get list of dependencies for npm and yarn package.
  
    Args:
        package (str): The package name for the npm/yarn package you want to install.

    Return:
        list. A list of all dependencies found.

    Exemple:

    .. code-block:: python
        
        >>> from getdep import getdep 
        >>> getdep.get_npm_dependencies("express")
        ['accepts', 'array-flatten', 'body-parser', 'content-disposition', 'content-type', 'cookie', 'cookie-signature',
         'debug', 'depd', 'encodeurl', 'escape-html', 'etag', 'finalhandler', 'fresh', 'merge-descriptors', 'methods', 
         'on-finished', 'parseurl', 'path-to-regexp', 'proxy-addr', 'qs', 'range-parser', 'safe-buffer', 'send', 'serve-static', 
         'setprototypeof', 'statuses', 'type-is', 'utils-merge', 'vary']
    
    """

    npmDependencies = []
    p = utility.get_dependencies("npm", package)
    try :
        npmDependencies = json.loads(p.text)["dependencies"]

    except UnboundLocalError:
        print("Your Package Management System : is not supported")
        utility.print_supported_pms()
        return []
    except KeyError:
        # no dependencies found
        if p.status_code == 200:
            return []
    except json.decoder.JSONDecodeError:
            print("Package not found on npm")
            return []
    
    return [word.split(':')[0] for word in npmDependencies]

# Use for chocolatey and Nuget
def get_chocolatey_dependencies(package):
    """Get list of dependencies for nuget and chocolatey
  
    Args:
        package (str): The package name for the nuget or chocolatey package you want to install.

    Return:
        list. A list of all dependencies found.

    Exemple:

    .. code-block:: python
        
        >>> from getdep import getdep 
        >>> getdep.get_chocolatey_dependencies("castle.core")
        >>> getdep.get_chocolatey_dependencies("castle.core")
        ['.NETStandard1.3', '.NETFramework4.5', '.NETFramework3.5', '.NETFramework4.0', '.NETStandard1.5']

    TODO: separate nuget and chocolatey implementation
    
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

def get_brew_dependencies(package):
    """Get list of dependencies from homebrew package.

    Args:
        package (str): The package name for the brew formulae you want to install.

    Return:
        list. A list of all dependencies found.

    Exemple:

    .. code-block:: python
        
        >>> from getdep import getdep 
        >>> getdep.get_brew_dependencies("vim")
        ['gettext', 'lua', 'perl', 'python', 'ruby']

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

# Used for RPM-based Linux distributions (fedora, CentOS). Basicaly any package using rpm and yum (soon DNF)
def get_yum_dependencies(package):
    """Get list of dependencies from yum command

    Also apply for RPM-based Linux distribution like Fedora, SuSE, CentOS
    
    Args:
        package (str): The package name for the apt package you want to install

    Return:
        list. A list of all dependencies found.

    Exemple:

    .. code-block:: python
        
        >>> from getdep import getdep 
        >>> getdep.get_yum_dependencies("rust")
        ['gcc-8.3.1-5.el8.0.2.x86_64', 'glibc-2.28-101.el8.i686', 'llvm-libs-9.0.1-4.module_el8.2.0+309+0c7b6b03.x86_64', 'rust-std-static(x86-64)', 
        'glibc-2.28-101.el8.x86_64', 'libgcc-8.3.1-5.el8.0.2.x86_64', 'libstdc++-8.3.1-5.el8.0.2.x86_64']


    """
    
    yumDependencies = []
    p = utility.get_dependencies("yum", package)
    # filter packages
    output = p.stdout.split()[2:-1]

    # 3 : start with the first provider. A step for 4 to skip : "dependency" string, the dependency and the "provider" string
    # remove double with set (cause of i386 and x64 of same dependency)
    yumDependencies = list(set([output[i] for i in range(3,len(output),4)]))

    return yumDependencies

# TODO: pacman PMS
#def get_pacman_dependencies(package):
#    pass



## depreciated
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