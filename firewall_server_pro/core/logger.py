from models.captured_packet import CapturedPacket


class Logger:

    def __init__(self, log_file_name="firewall.log"):
        self.log_file_name = log_file_name
        self.logged_connections = set()

    def log_event(self, packet_event: CapturedPacket):

        key = (
            packet_event.source_ip,
            packet_event.destination_ip,
            packet_event.destination_port
        )

        if key in self.logged_connections:
            return

        self.logged_connections.add(key)

        line = (
            f"[BLOCKED {packet_event.direction}] "
            f"{packet_event.transport_protocol}/"
            f"{packet_event.application_protocol} | "
            f"{packet_event.destination_ip}:"
            f"{packet_event.destination_port}"
        )

        with open(self.log_file_name, "a") as f:
            f.write(line + "\n")
