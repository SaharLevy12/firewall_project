import psutil
import threading
import time

class Scanner:
    def __init__(self, interval=1):
        self.interval = interval
        self.current_connections = []
        self.lock = threading.Lock()
        self.running = False

    def start(self):
        if not self.running:
            self.running = True
            thread = threading.Thread(target=self._update_loop, daemon=True)
            thread.start()

    def _update_loop(self):
        while self.running:
            self._update_connections()
            time.sleep(self.interval)

    def _update_connections(self):
        connections = []

        for conn in psutil.net_connections(kind="inet"):
            if not conn.laddr or not conn.pid or conn.status != psutil.CONN_ESTABLISHED:
                continue

            try:
                process_name = psutil.Process(conn.pid).name()
            except:
                process_name = "unknown"

            connections.append({
                "process_name": process_name,
                "process_id": conn.pid,
                "status": conn.status,
                "local_ip": conn.laddr.ip,
                "local_port": conn.laddr.port,
                "remote_ip": conn.raddr.ip if conn.raddr else None,
                "remote_port": conn.raddr.port if conn.raddr else None
            })

        with self.lock:
            self.current_connections = connections

    def get_current_connections(self):
        with self.lock:
            return list(self.current_connections)