import socket, threading, json, os, queue
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import wx


class PolicyClient:
    def __init__(self, enforcer, host="127.0.0.1", port=8080):
        self.enforcer = enforcer
        self.username = None
        self.is_admin = False

        self.host = host
        self.port = port

        self.sock = socket.socket()
        self.session_key = None

        self.gui = None
        self.gui_queue = queue.Queue()

    def connect(self):
        self.sock.connect((self.host, self.port))

        public_key_pem = self.sock.recv(4096)
        public_key = serialization.load_pem_public_key(public_key_pem)

        self.session_key = os.urandom(32)

        encrypted_key = public_key.encrypt(
            self.session_key,
            padding.OAEP(
                mgf=padding.MGF1(hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        self.sock.send(encrypted_key)

        threading.Thread(target=self.listen_updates, daemon=True).start()

    def encrypt(self, msg):
        aes = AESGCM(self.session_key)
        nonce = os.urandom(12)
        return nonce + aes.encrypt(nonce, msg.encode(), None)

    def decrypt(self, data):
        aes = AESGCM(self.session_key)
        nonce, ciphertext = data[:12], data[12:]
        return aes.decrypt(nonce, ciphertext, None).decode()

    def listen_updates(self):
        while True:
            try:
                data = self.sock.recv(4096)
                msg = self.decrypt(data)
                self.gui_queue.put(msg)
            except:
                continue

    def disconnect(self):
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except:
            pass

        try:
            self.sock.close()
        except:
            pass

    def command_update_rules(self, new_rules):
        msg = f"update rules|{self.username}|{json.dumps(new_rules)}"
        self.sock.send(self.encrypt(msg))