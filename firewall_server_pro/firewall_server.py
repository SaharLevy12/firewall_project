import socket
import threading
from datetime import datetime

from core.firewall_engine import FirewallEngine
from models.captured_packet import CapturedPacket

firewall = FirewallEngine(r"firewall_server_pro/firewall_config.json")


def relay(src, dst):
    try:
        while True:
            data = src.recv(4096)
            if not data:
                break
            dst.sendall(data)
    except:
        pass
    finally:
        src.close()
        dst.close()


def handle_client(client):
    try:
        line = client.recv(1024).decode().strip()
        cmd, host, port = line.split()
        port = int(port)

        packet_event = CapturedPacket(
            timestamp=datetime.now(),
            direction="OUT",
            source_ip="CLIENT",
            source_port=0,
            destination_ip=host,
            destination_port=port,
            transport_protocol="TCP",
            application_protocol="",
            payload_size=0
        )

        allowed = firewall.process_packet(None, packet_event)

        if not allowed:
            client.send(b"BLOCK\n")
            client.close()
            print("[BLOCKED]", host, port)
            return

        client.send(b"ALLOW\n")

        remote = socket.socket()
        remote.connect((host, port))

        print("[ALLOWED]", host, port)

        threading.Thread(target=relay, args=(client, remote)).start()
        threading.Thread(target=relay, args=(remote, client)).start()

    except Exception as e:
        print("Error:", e)
        client.close()


server = socket.socket()
server.bind(("0.0.0.0", 9000))
server.listen(20)

print("🔥 Firewall Server running on port 9000")

while True:
    client, _ = server.accept()
    threading.Thread(target=handle_client, args=(client,)).start()
