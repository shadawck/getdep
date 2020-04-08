from getdep import getdep
import collections
import functools

# Test getdep for all method (pip, gem, composer...)
class TestGetdep:

    def c_list(self,list1, list2):
        return(functools.reduce(lambda i, j : i and j, map(lambda m, k: m == k, list1, list2), True))


    def test_getAptDependencies(self):
        package = 'nano'
        cst_dep = ['libc6', 'libncursesw5', 'libtinfo5', 'libgcc1', 'gcc-8-base']

        dep = getdep.get_apt_dependencies(package)

        assert set(cst_dep) == set(dep)


    def test_getPipDependencies(self):
        package = 'requests'
        cst_dep = ['chardet', 'idna', 'urllib3', 'certifi', 'pyOpenSSL', 'cryptography', 'PySocks', 'win-inet-pton']
        
        dep = getdep.get_pip_dependencies(package)
        
        assert set(cst_dep) == set(dep)


    def test_getComposerDependencies(self):
        package = "laravel/installer"
        cst_dep = ['php', 'ext-zip', 'guzzlehttp/guzzle', 'symfony/console', 'symfony/filesystem', 'symfony/process']

        dep = getdep.get_composer_dependencies(package)

        assert set(cst_dep) == set(dep)
    
    def test_getNpmDependencies(self):
        package = "gulp"
        cst_dep = ['glob-watcher', 'gulp-cli', 'undertaker', 'vinyl-fs']

        dep = getdep.get_npm_dependencies(package)

        assert set(cst_dep) == set(dep)
    
    def test_getGemDependencies(self):
        package = "globalize"
        cst_dep = ["activemodel", "activerecord", "request_store"]
        dep = getdep.get_gem_dependencies(package)

        assert set(cst_dep) == set(dep)