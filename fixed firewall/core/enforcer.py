import json
from models.captured_packet import CapturedPacket

class Enforcer:
    def __init__(self, config_file: str = "firewall_config.json"):
        self.blocked_ports = set()
        self.blocked_protocols = set()
        self.load_config(config_file)

    def load_config(self, config_file: str):
        try:
            with open(config_file, "r") as f:
                config = json.load(f)
            for port in config.get("blocked_ports", []):
                self.blocked_ports.add(port)
            for protocol in config.get("blocked_protocols", []):
                self.blocked_protocols.add(protocol)
        except FileNotFoundError:
            print(f"Config file {config_file} not found, using empty rules")

    def should_block(self, packet_event: CapturedPacket) -> bool:
        if packet_event.source_port in self.blocked_ports:
            return True
        if packet_event.destination_port in self.blocked_ports:
            return True
        if packet_event.application_protocol in self.blocked_protocols:
            return True
        return False
