import json
import socket
from models.captured_packet import CapturedPacket

class Enforcer:
    def __init__(self, config_file):
        self.blocked_port_set = set()
        self.blocked_protocol_set = set()
        self.blocked_domain_set = set()
        self.blocked_domain_ip_cache = {}  # domain -> set of IPs
        self.load_config(config_file)
        self.resolve_blocked_domains()

    def load_config(self, config_file):
        try:
            with open(config_file, "r") as f:
                config = json.load(f)
                self.blocked_port_set = set(config.get("blocked_ports", []))
                self.blocked_protocol_set = set(config.get("blocked_protocols", []))
                self.blocked_domain_set = set(config.get("blocked_domains", []))
        except FileNotFoundError:
            print("Config not found")

    def resolve_blocked_domains(self):
        for domain in self.blocked_domain_set:
            try:
                ips = socket.gethostbyname_ex(domain)[2]  # returns list of IPs matching to the requested domain
                self.blocked_domain_ip_cache[domain] = set(ips)
            except Exception as e:
                print(f"[ERROR] Failed to resolve {domain}: {e}")

    def is_destination_ip_blocked(self, packet_event: CapturedPacket):
        for domain, ips in self.blocked_domain_ip_cache.items():
            if packet_event.destination_ip in ips:
                return True
        return False

    def should_block(self, raw_packet, packet_event: CapturedPacket):
        # Check destination port
        if packet_event.source_port in self.blocked_port_set:
            return True
        if packet_event.destination_port in self.blocked_port_set:
            return True

        # Check application protocol
        if packet_event.application_protocol in self.blocked_protocol_set:
            return True

        # Check blocked IPs
        if self.is_destination_ip_blocked(packet_event):
            return True

        return False