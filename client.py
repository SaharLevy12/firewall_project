import socket
from cryptography.hazmat.primitives import serialization

class Client:
    def __init__(self, ip="127.0.0.1", port=8080):
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sock.connect((ip, port))
        public_pem = self.client_sock.recv(4096)
        self.public_key = serialization.load_pem_public_key(public_pem)

    def send_data(self, msg):
        self.client_sock.send(msg.encode())

    def send_encrypted_data(self,msg):
        self.client_sock.send(msg)

    def recv_data(self):
        return self.client_sock.recv(1024).decode()

    def close(self):
        self.client_sock.close()
