import json
from models.captured_packet import CapturedPacket


class Enforcer:
    def __init__(self, config_file):
        self.blocked_ports = set()
        self.blocked_protocols = set()
        self.load_config(config_file)

    def load_config(self, config_file: str):
        try:
            with open(config_file, "r") as f:
                config = json.load(f)

            self.blocked_ports = set(config.get("blocked_ports", []))
            self.blocked_protocols = set(config.get("blocked_protocols", []))

        except FileNotFoundError:
            print("Config not found — using empty rules")

    def should_block(self, packet_event: CapturedPacket):

        if packet_event.destination_port in self.blocked_ports:
            return True

        if packet_event.application_protocol in self.blocked_protocols:
            return True

        return False
