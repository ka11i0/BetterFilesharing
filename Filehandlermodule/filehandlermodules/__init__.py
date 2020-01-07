import pkgutil
import sys
import os, glob, importlib

# List that contains the name of all found modules
filehandlermodules = []

def loadModule(moduleName):
    module = None
    try:
        import sys
        del sys.modules[moduleName]
    except BaseException as err:
        pass
    try:
        import importlib
        print(__module__)
        module = importlib.import_module('.'+moduleName, __module__)
    except BaseException as err:
        serr = str(err)
        print("Error to load the module '" + moduleName + "': " + serr)
    return module

def reloadModule(moduleName):
    module = loadModule(moduleName)
    moduleName, modulePath = str(module).replace("' from '", "||").replace("<module '", '').replace("'>", '').split("||")
    if (modulePath.endswith(".pyc")):
        import os
        os.remove(modulePath)
        module = loadModule(moduleName)
    return module

def getInstance(className):
    module = reloadModule(className.lower())
    Class = getattr(module, className)
    instance = Class()
    return instance

def load_all_modules():
    modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
    modules = [os.path.basename(f)[:-3] for f in modules if not f.endswith("__init__.py")]
    for f in modules:
        loadModule(f)
        filehandlermodules.append(f)

#load_all_modules()
modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
__all__ = [os.path.basename(f)[:-3] for f in modules if not f.endswith("__init__.py")]
