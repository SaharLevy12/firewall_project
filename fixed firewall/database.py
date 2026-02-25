import sqlite3
import threading

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(r"fixed firewall/Users.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, email TEXT, password TEXT)')
        self.conn.commit()
        self.lock = threading.Lock()
    
    def register_user(self, request):
        _, username, email, password = request.split(",")

        with self.lock:
            self.cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (username, email, password))
            self.conn.commit()
        return

    def check_login(self, request):
        _, email, password = request.split(",")

        with self.lock:
            self.cursor.execute("SELECT username FROM users WHERE email=? AND password=?", (email, password))
            result = self.cursor.fetchone()

        if result:
            return ("valid", result[0])
        return ("invalid", None)
