import socket
import select
import json
import os
import threading
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from database import Database

INITIAL_RULES = {
    "blocked_ports": [],
    "blocked_protocols": [],
    "blocked_domains": []
}

HOST = "0.0.0.0"
PORT = 8080

class Server:
    def __init__(self):
        self.clients = {}
        self.private_key = self.create_rsa_private_key()
        self.public_key = self.create_rsa_public_key(self.private_key)
        self.open_sockets = []
        self.database = Database()

    def create_rsa_private_key(self):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        return private_key
    
    def create_rsa_public_key(self,private_key):
        return private_key.public_key()
    
    def encrypt_aes(self,session_key, plaintext):
        aes = AESGCM(session_key)
        nonce = os.urandom(12)
        return nonce + aes.encrypt(nonce, plaintext.encode(), None)
    
    def decrypt_aes(self,session_key, data):
        aes = AESGCM(session_key)
        nonce, ciphertext = data[:12], data[12:]
        return aes.decrypt(nonce, ciphertext, None).decode()
    
    def send_rules(self,sock, session_key):
        msg = "rules " + json.dumps(INITIAL_RULES)
        sock.send(self.encrypt_aes(session_key, msg))
        print("sent rules to client..") 
    
    def broadcast_rules(self):
        for sock, client in self.clients.items():
            self.send_rules(sock, client["session_key"])
        print("broadcasted")
    
    def open_socket(self):
        listening_socket = socket.socket()
        listening_socket.bind((HOST, PORT))
        listening_socket.listen(1)
        print(f"Policy Server listening on {HOST}:{PORT}")
        return listening_socket
    
    
    def listen_to_clients(self,server_socket):
        while True:
            all_socks = [server_socket] + self.open_sockets
            rlist, wlist, xlist = select.select(all_socks, all_socks, [])
            for sock in rlist:
                if sock is server_socket:
                    client_sock, addr = sock.accept()
                    print("Client connected:", addr)
                    self.open_sockets.append(client_sock)
                    public_key_pem = self.public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo)
                    client_sock.send(public_key_pem)

                else:
                    data = sock.recv(4096)

                    if sock not in self.clients:
                        session_key = self.private_key.decrypt(
                            data,
                            padding.OAEP(
                                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                algorithm=hashes.SHA256(),
                                label=None
                            )
                        )
                        self.clients[sock] = {"session_key":session_key,
                                              "username":None,
                                              "admin":False
                        }
                        
                    else:
                        client = self.clients[sock]
                        session_key = client["session_key"]
                        message = self.decrypt_aes(session_key, data)
                        
                        if "login" in message:
                            is_valid, username = self.database.check_login(message)
                            if is_valid == "valid":
                                client["username"] = username
                                if client["username"] == "sahar":
                                    client["admin"] = 1
                                else:
                                    client["admin"] = 0
                                sock.send(self.encrypt_aes(session_key,f"login success|{username}|{client["admin"]}"))
                                self.send_rules(sock, session_key)

                            else:
                                pass
                        if "register" in message:
                            self.database.register_user(message)
                            sock.send(self.encrypt_aes(session_key,"register success"))

                        if message.startswith("get rules"):
                            self.send_rules(sock, session_key)

                        elif message.startswith("update rules"):
                            json_rules = message.split("|")[2]
                            new_rules = json.loads(json_rules)
                            INITIAL_RULES.update(new_rules)
                            print("[SERVER] Rules updated:", INITIAL_RULES)
                            self.broadcast_rules()
                            
if __name__ == "__main__":
    server = Server()
    server_socket = server.open_socket()
    
    server_thread = threading.Thread(target=server.listen_to_clients, args=(server_socket,))
    server_thread.start()
