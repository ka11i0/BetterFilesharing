import socket

class FileReciever:
    def __init__(self, host, port):
        self.host = host
        self.port = port
    
    def start(self, filepath, writeargs):
        data = bytes()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            
            conn, addr = s.accept()
            print("Client connected")
            with conn:
                while True:
                    chunk = conn.recv(1024)
                    if not chunk:
                        conn.sendall("thanks".encode())
                        break
                    data += chunk
        
        print("Connection closed") 
        with open(filepath, writeargs) as file:
            file.write(data.decode())
