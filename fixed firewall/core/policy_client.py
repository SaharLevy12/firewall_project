
import socket, threading, json, os
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import wx
from pages.firewall_gui import FirewallGUI
from core.main_gui import MainGUI
from datetime import datetime


class PolicyClient:
    def __init__(self, enforcer, host="127.0.0.1", port=8080):
        self.enforcer = enforcer
        self.username = None
        self.is_admin = None
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
            padding.OAEP(mgf=padding.MGF1(hashes.SHA256()),
                         algorithm=hashes.SHA256(),
                         label=None)
        )
        self.sock.send(encrypted_key)
                
        threading.Thread(target=self.check_curfew, daemon=True).start()        
        threading.Thread(target=self.listen_updates, daemon=True).start()

    def encrypt(self, msg):
        aes = AESGCM(self.session_key)
        nonce = os.urandom(12)
        return nonce + aes.encrypt(nonce, msg.encode(), None)

    def decrypt(self, data):
        aes = AESGCM(self.session_key)
        nonce, ciphertext = data[:12], data[12:]
        return aes.decrypt(nonce, ciphertext, None).decode()
    
    def check_curfew(self):
        time = datetime.now()
        hours = time.hour
        if hours == 17:
            self.enforcer.enable_curfew()

    def listen_updates(self):
        while True:
            try:
                data = self.sock.recv(4096)
                msg = self.decrypt(data)
                if msg.startswith("rules"):
                    rules = json.loads(msg[len("rules "):])
                    print("rules: ", rules)
                    self.enforcer.update_rules(rules)
                    wx.CallAfter(self.gui.panels["firewall"].refresh_lists(self))

                if msg == "go to sleep ASAP!":
                    self.enforcer.enable_curfew()

                if msg.startswith("login success"):
                    _,username,is_admin = msg.split("|")
                    if is_admin == "0":
                        is_admin = False
                    else:
                        is_admin = True
                    self.username = username
                    self.is_admin = is_admin
                    wx.CallAfter(self.gui.show_firewall)
                
                if msg.startswith("register success"):
                    wx.MessageBox("Register completed successfully!", "Register", wx.OK | wx.ICON_INFORMATION)
            except:
                continue

    def command_update_rules(self, new_rules):
            msg = f"update rules|{self.username}|{json.dumps(new_rules)}"
            self.sock.send(self.encrypt(msg))