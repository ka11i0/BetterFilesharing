from .defaultmodule import Defaultmodule
class Abcmodule(Defaultmodule):
    def writedata(self, filepath, data, writeargs='w'):
        print("in Abc")
        with open(filepath, writeargs) as file:
            file.write(data)

    def readdata(self, filepath):
        with open(filepath, 'r') as file:
            data = file.read()
        return data

    def typesupported(self, filetype):
        if filetype in ["abc", "abd", "abe"]:
            return True
        return False
