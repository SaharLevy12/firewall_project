import socket
import select
import json
import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

RULES = {
    "blocked_ports": [21, 25, 587],
    "blocked_protocols": ["FTP", "SMTP"],
    "blocked_domains": ["facebook.com", "example.com"]
}

clients = {}  # {socket: session_key}

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()
public_key_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

def encrypt_aes(session_key, plaintext: str) -> bytes:
    aes = AESGCM(session_key)
    nonce = os.urandom(12)
    return nonce + aes.encrypt(nonce, plaintext.encode(), None)

def decrypt_aes(session_key, data: bytes) -> str:
    aes = AESGCM(session_key)
    nonce, ciphertext = data[:12], data[12:]
    return aes.decrypt(nonce, ciphertext, None).decode()

def send_rules(sock, session_key):
    msg = "RULES " + json.dumps(RULES)
    sock.send(encrypt_aes(session_key, msg))

def broadcast_rules():
    for sock, session_key in clients.items():
        send_rules(sock, session_key)


HOST = "0.0.0.0"
PORT = 8080

server_sock = socket.socket()
server_sock.bind((HOST, PORT))
server_sock.listen(5)
print(f"Policy Server listening on {HOST}:{PORT}")

open_sockets = [server_sock]

while True:
    readable, _, _ = select.select(open_sockets, [], [])

    for sock in readable:
        if sock is server_sock:
            client_sock, addr = server_sock.accept()
            print("Client connected:", addr)
            open_sockets.append(client_sock)
            client_sock.send(public_key_pem)

        else:
            try:
                data = sock.recv(4096)
                if not data:
                    open_sockets.remove(sock)
                    clients.pop(sock, None)
                    sock.close()
                    continue

                if sock not in clients:
                    session_key = private_key.decrypt(
                        data,
                        padding.OAEP(
                            mgf=padding.MGF1(algorithm=hashes.SHA256()),
                            algorithm=hashes.SHA256(),
                            label=None
                        )
                    )
                    clients[sock] = session_key
                    send_rules(sock, session_key)

                else:
                    session_key = clients[sock]
                    message = decrypt_aes(session_key, data)

                    if message.startswith("GET_RULES"):
                        send_rules(sock, session_key)

                    elif message.startswith("UPDATE_RULES"):
                        _, json_rules = message.split("|", 1)
                        new_rules = json.loads(json_rules)
                        RULES.update(new_rules)
                        print("[SERVER] Rules updated:", RULES)
                        broadcast_rules()

            except Exception as e:
                print("Client error:", e)
                open_sockets.remove(sock)
                clients.pop(sock, None)
                sock.close()