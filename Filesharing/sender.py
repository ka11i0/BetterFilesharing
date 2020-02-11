import socket
from Filehandlermodule.filehandler import Filehandler

class FileSender:
    def __init__(self, host="127.0.0.1", port="80"):
        self.host = host
        self.port = port
    
    def sendfile(self, filepath):
        fh = Filehandler()
        data = fh.read(filepath)
        
        print("Data read proceeding with sending")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(data.encode())
            print("Data sent")
        print("Done for the day")
