import socket
from Filehandlermodule.filehandler import Filehandler

class FileReceiver:
    def __init__(self, host, port):
        # The address and port that the socket should bind to
        self.host = host
        self.port = port
    
    def start(self, filepath):
        # byte array to store incomming message
        data = bytes()
        # Create a socket that will recieve the incomming message
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Bind socket to address and port
            s.bind((self.host, self.port))
            # Set timeout to stop with the listening after 5 seconds
            s.settimeout(5)
            # Start listening after connections, at most 20 connections can connect and queue
            s.listen(20)
            
            try:
                # accept the first connection in the queue
                conn, addr = s.accept()
                # as long as the connection is active
                with conn:
                    # continue to read a chunk at a time
                    while True:
                        # read chunk
                        chunk = conn.recv(1024)
                        # if the chunk does not contain anything
                        if not chunk:
                            # be polite and say thank you to the sender
                            conn.sendall("thanks".encode())
                            # stop reading 
                            break
                        # add read chunk to the complete message stored in data
                        data += chunk
            except socket.timeout as e:
                # happens when no connection is made, close the socket and send the problem up to handle it
                s.close()
                raise Exception("Something went wrong with the filetransfer")
        
        # create a filehandler to store the data that was in the message
        fh = Filehandler()
        fh.writedata(filepath, data.decode())
 
