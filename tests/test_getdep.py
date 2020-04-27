from getdep import getdep
import collections
import functools

# Test getdep for all method (pip, gem, composer...)
class TestGetdep:
    
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
    
    def test_getYarnDependencies(self):
        package = "gulp"
        cst_dep = ['glob-watcher', 'gulp-cli', 'undertaker', 'vinyl-fs']

        dep = getdep.get_yarn_dependencies(package)

        assert set(cst_dep) == set(dep)
    
    def test_getGemDependencies(self):
        package = "globalize"
        cst_dep = ["activemodel", "activerecord", "request_store"]
        dep = getdep.get_gem_dependencies(package)

        assert set(cst_dep) == set(dep)
    
    def test_getChocoDependencies(self):
        package = "BCrypt.Net-Next"
        cst_dep = ['.NETFramework2.0', '.NETFramework4.5.2', '.NETFramework3.5', '.NETFramework4.6.2', '.NETFramework4.7.2', '.NETFramework4.0', '.NETStandard2.1', '.NETStandard2.0']
        dep = getdep.get_chocolatey_dependencies(package)

        assert set(cst_dep) == set(dep)
    

    def test_getBrewDependencies(self):
        package = "sqlite"
        cst_dep = ['readline']
        dep = getdep.get_brew_dependencies(package)

        assert set(cst_dep) == set(dep)
    