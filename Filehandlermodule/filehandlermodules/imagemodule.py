from .defaultmodule import Defaultmodule
import base64

#differes with default by read/write-ing bytewise, rb = readbyte, wb = writebyte
class Imagemodule(Defaultmodule):
    def writedata(self, filepath, data, writeargs='wb'):
        with open(filepath, writeargs) as file:
            file.write(data.fromhex())

    def readdata(self, filepath):
        with open(filepath, 'rb') as file:
            return file.read().hex()

#only tested with these two formats
    def typesupported(self, filetype):
        if filetype in ["png", "jpg"]:
            return True
        return False