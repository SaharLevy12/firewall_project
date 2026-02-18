import pydivert
import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9000

connections = {}


def ask_firewall(dst_ip, dst_port):
    sock = socket.socket()
    sock.connect((SERVER_IP, SERVER_PORT))

    msg = f"CONNECT {dst_ip} {dst_port}\n"
    sock.send(msg.encode())

    decision = sock.recv(32).decode().strip()

    if decision == "BLOCK":
        sock.close()
        return None

    return sock


print("Transparent client running")

with pydivert.WinDivert("ip") as w:
    for packet in w:
        key = (packet.dst_addr, packet.dst_port)

        if key not in connections:
            tunnel = ask_firewall(packet.dst_addr, packet.dst_port)

            if tunnel is None:
                print("Blocked:", key)
                continue

            connections[key] = tunnel
