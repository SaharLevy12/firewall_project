
import socket, threading, json, os
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class PolicyClient:
    def __init__(self, enforcer, username="admin", is_admin=True, host="192.168.1.228", port=8080):
        self.enforcer = enforcer
        self.username = username
        self.is_admin = is_admin
        self.host = host
        self.port = port
        self.sock = socket.socket()
        self.session_key = None
        self.gui = None

    def connect(self):
        self.sock.connect((self.host, self.port))
        public_key_pem = self.sock.recv(4096)
        public_key = serialization.load_pem_public_key(public_key_pem)

        self.session_key = os.urandom(32)
        encrypted_key = public_key.encrypt(
            self.session_key,
            padding.OAEP(mgf=padding.MGF1(hashes.SHA256()),
                         algorithm=hashes.SHA256(),
                         label=None)
        )
        self.sock.send(encrypted_key)

        self._receive_rules_once()
        threading.Thread(target=self._listen_updates, daemon=True).start()

    def _encrypt(self, msg: str) -> bytes:
        aes = AESGCM(self.session_key)
        nonce = os.urandom(12)
        return nonce + aes.encrypt(nonce, msg.encode(), None)

    def _decrypt(self, data: bytes) -> str:
        aes = AESGCM(self.session_key)
        nonce, ciphertext = data[:12], data[12:]
        return aes.decrypt(nonce, ciphertext, None).decode()

    def _receive_rules_once(self):
        data = self.sock.recv(4096)
        msg = self._decrypt(data)
        if msg.startswith("RULES"):
            rules = json.loads(msg[len("RULES "):])
            self.enforcer.update_rules(rules)

    def _listen_updates(self):
        while True:
            try:
                data = self.sock.recv(4096)
                msg = self._decrypt(data)
                if msg.startswith("RULES"):
                    rules = json.loads(msg[len("RULES "):])
                    self.enforcer.update_rules(rules)
                    if self.gui:
                        import wx
                        wx.CallAfter(self.gui.refresh_lists)
            except:
                continue

    def update_rules(self, new_rules: dict):
        if not self.is_admin:
            print("Only admin can update rules")
            return
        msg = f"UPDATE_RULES|{self.username}|{json.dumps(new_rules)}"
        self.sock.send(self._encrypt(msg))