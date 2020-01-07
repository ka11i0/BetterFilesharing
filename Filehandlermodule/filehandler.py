#from filehandlermodules import *
from Filehandlermodule.filehandlermodules import *
import Filehandlermodule.filehandlermodules
import sys
class Filehandler:
    def __init__(self):
        # Declare a list of the different handler modules
        self.handlers = list()
        print()
        # For each module in the loaded handler modules
        for modulename in Filehandlermodule.filehandlermodules.__all__:
            # Take away __init__ and defaultmodule (we take away defaultmodule as that should be last)
            if not modulename.startswith('__') and not modulename.startswith("defaultmodule"):
                classname = modulename[0].upper() + modulename[1:]
                # Get the instance of the handler module and append it in the handler list
                module = sys.modules["Filehandlermodule.filehandlermodules."+modulename]
                Class = getattr(module, classname)
                self.handlers.append(Class())
        # Add the defaultmodule last in the list
        module = sys.modules["Filehandlermodule.filehandlermodules.defaultmodule"]
        Class = getattr(module, "Defaultmodule")
        self.handlers.append(Class()) 
    # Private function that takes out a handler that can handle the requested file
    def __gethandler(self, filepath):
        # Parse the filetype
        filetype = filepath.split('.')[-1]
        for handler in self.handlers:
            # Check if the handler supports the requested filetype default handler always returns true
            if handler.typesupported(filetype=filetype):
                return handler
        return None
    
    # Writes the data using a handler that supports the file
    def writedata(self, filepath, data):
        # Get a handler that supports the given file
        handler = self.__gethandler(filepath)
        # Use the handler to write the data
        handler.writedata(filepath, data)
    
    # Reads data using a hander that supports the file
    def readdata(self, filepath):
        # Get a handler that supports the given file
        handler = self.__gethandler(filepath)
        # Use the handler to read the data
        data = handler.readdata(filepath)
        return data
