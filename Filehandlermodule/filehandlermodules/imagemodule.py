from .defaultmodule import Defaultmodule

#differes with default by read/write-ing bytewise, rb = readbyte, wb = writebyte
class Imagemodule(Defaultmodule):
    def writedata(self, filepath, data, writeargs='wb'):
        with open(filepath, writeargs) as file:
            file.write(data.encode())

    def readdata(self, filepath):
        with open(filepath, 'rb') as file:
            return file.read().decode()

#only tested with these two formats
    def typesupported(self, filetype):
        if filetype in ["png", "jpg"]:
            return True
        return False