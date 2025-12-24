import socket, select
import threading
import websockets
import asyncio
from waf_utilities import WAF_Utilities
from database import Database
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

    async def handler(self,websocket):
        print("Client connected!")
        async for message in websocket:
            print("Received:", message)
            if "login" in message:
                loaded_message = json.loads(message)
                is_valid,status = WAF_Utilities.check_sql_injection(loaded_message)
                response = {
                    "action":f"{loaded_message["action"]}",
                    "username":f"{loaded_message["username"]}",
                    "status":f"{status}"
                }
                await websocket.send(json.dumps(response))


    async def listen_to_web_clients(self):
        async with websockets.serve(self.handler, "0.0.0.0", 9999):
            print(f"WebSocket server started on ws://{"0.0.0.0"}:9999")
            await asyncio.Future()  

    def start_listen_to_web_clients(self):
        asyncio.run(self.listen_to_web_clients())
        
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
    web_thread = threading.Thread(target=server.start_listen_to_web_clients)
    tcp_thread.start()
    web_thread.start()
