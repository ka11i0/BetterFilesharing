class Defaultmodule:
    def writedata(self, filepath, data, writeargs='w'):
        with open(filepath, writeargs) as file:
            file.write(data)
    
    def readdata(self, filepath):
        with open(filepath, 'r') as file:
            data = file.read()
        return data
    
    def typesupported(self, filetype):
        return True
