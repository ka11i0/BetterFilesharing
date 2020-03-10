import socket
from Filehandlermodule.filehandler import Filehandler

class FileSender:
    def __init__(self, host="127.0.0.1", port="80"):
        # set host and port for which the socket should connect to
        self.host = host
        self.port = port
    
    def start(self, filepath):
        # create a file handler that can handle the file type
        fh = Filehandler()
        data = fh.readdata(filepath)
        
        # Create a socket that will receive the file
        print("Data read proceeding with sending")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                # set timeout for connectiong to 5 seconds
                s.settimeout(5)
                # try to connect to host
                s.connect((self.host, self.port))
                # connection established, send file
                s.sendall(data.encode())
                print("Data sent")
            except socket.timeout as e:
                # timeout reached something went wrong
                s.close()
                raise Exception("Something went wrong with the filetransfer")
        print("Done for the day")
