import socket, select, json, os
from cryptography.hazmat.primitives.asymmetric import padding, serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes

class PolicyClient:
    def __init__(self, enforcer, host="127.0.0.1", port=8080):
        self.enforcer = enforcer
        self.host = host
        self.port = port
        self.sock = socket.socket()
        self.session_key = None

    def connect(self):
        self.sock.connect((self.host, self.port))

        public_key_pem = self.sock.recv(4096)
        public_key = serialization.load_pem_public_key(public_key_pem)

        self.session_key = os.urandom(32)
        encrypted_key = public_key.encrypt(
            self.session_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        self.sock.send(encrypted_key)

        self.receive_rules_once()

    def encrypt(self, msg):
        aes = AESGCM(self.session_key)
        nonce = os.urandom(12)
        return nonce + aes.encrypt(nonce, msg.encode(), None)

    def decrypt(self, data):
        aes = AESGCM(self.session_key)
        nonce = data[:12]
        ciphertext = data[12:]
        return aes.decrypt(nonce, ciphertext, None).decode()

    def receive_rules_once(self):
        data = self.sock.recv(4096)
        if not data:
            return
        message = self.decrypt(data)
        if message.startswith("RULES"):
            rules_json = message[len("RULES "):]
            rules = json.loads(rules_json)
            self.enforcer.update_rules(rules)
            print("[PolicyClient] Rules received:", rules)

    def request_rules(self):
        self.sock.send(self.encrypt("GET_RULES"))

    def update_rules(self, new_rules: dict):
        msg = "UPDATE_RULES|" + json.dumps(new_rules)
        self.sock.send(self.encrypt(msg))