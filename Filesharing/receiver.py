import socket
from Filehandlermodule.filehandler import Filehandler

class FileReceiver:
    def __init__(self, host, port):
        self.host = host
        self.port = port
    
    def start(self, filepath):
        data = bytes()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.timeout(5)
            s.listen(20)
            
            try:
                conn, addr = s.accept()
                with conn:
                    while True:
                        chunk = conn.recv(1024)
                        if not chunk:
                            conn.sendall("thanks".encode())
                            break
                        data += chunk
            except socket.timeout as e:
                s.close()
                raise Exception("Something went wrong with the filetransfer")
        
        fh = Filehandler()
        fh.writedata(filepath, data.decode())
 
