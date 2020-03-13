class Defaultmodule:
    # Data needs to be string
    def writedata(self, filepath, data, writeargs='w'):
        with open(filepath, writeargs) as file:
            file.write(data)
    
    # Need to return string
    def readdata(self, filepath):
        with open(filepath, 'r') as file:
            data = file.read()
        return data
    
    # Check if filetype is in supported filetypes
    def typesupported(self, filetype):
        return True
