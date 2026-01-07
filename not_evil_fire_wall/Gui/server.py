import socket, select
import threading
from Gui.database import Database
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
import json


class Server:

    def __init__(self):
        self.open_sockets = []
        self.data_base = Database()
        self.private_key = self.create_private_key()
        self.public_key = self.create_public_key(self.private_key)

    def open_socket(self):
        listening_socket = socket.socket()
        listening_socket.bind(("0.0.0.0", 8080))
        listening_socket.listen(1)
        print("TCP Server listening on port 8080")
        return listening_socket

    def listen_to_clients(self, listening_socket):
        while True:
            all_socks = [listening_socket] + self.open_sockets
            rlist, wlist, xlist = select.select(all_socks, all_socks, [])
            for sock in rlist:
                if sock is listening_socket:
                    client_socket, addr = listening_socket.accept()
                    print("TCP client connected:", addr)
                    self.open_sockets.append(client_socket)

                    public_pem = self.public_key.public_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo
                    )
                    client_socket.send(public_pem)

                else:
                    data = sock.recv(4096)
                    if not data:
                        self.open_sockets.remove(sock)
                        sock.close()
                        continue

                    data = self.decrypt(data, self.private_key).decode()
                    if "login" in data:
                        is_valid, username = self.data_base.check_login(data)
                        if is_valid == "valid":
                            sock.send(f"login successful,{username}".encode())
                        else:
                            sock.send(f"login denied,{username}".encode())
                    elif "register" in data:
                        self.data_base.register_user(data)
        
    def create_private_key(self):
        return rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

    def create_public_key(self, private):
        return private.public_key()

    def decrypt(self, encrypted, private_key):
        return private_key.decrypt(
            encrypted,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

if __name__ == "__main__":
    server = Server()
    sock = server.open_socket()
    
    tcp_thread = threading.Thread(target=server.listen_to_clients, args=(sock,))
    tcp_thread.start()
