import pkgutil
import sys
import os, glob, importlib

# List that contains the name of all found modules
modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
__all__ = [os.path.basename(f)[:-3] for f in modules if not f.endswith("__init__.py")]
