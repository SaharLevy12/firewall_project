import socket

class Enforcer:
    def __init__(self):
        self.blocked_port_set = set()
        self.blocked_protocol_set = set()
        self.blocked_domain_set = set()
        self.blocked_domain_ip_cache = {}

    def resolve_blocked_domains(self):
        self.blocked_domain_ip_cache = {}
        for domain in self.blocked_domain_set:
            try:
                ips = socket.gethostbyname_ex(domain)[2]
                self.blocked_domain_ip_cache[domain] = set(ips)
            except:
                pass

    def update_rules(self, rules):
        self.blocked_port_set = set(rules.get("blocked_ports", []))
        self.blocked_protocol_set = set(rules.get("blocked_protocols", []))
        self.blocked_domain_set = set(rules.get("blocked_domains", []))
        self.resolve_blocked_domains()

    def is_destination_ip_blocked(self, packet_event):
        for ips in self.blocked_domain_ip_cache.values():
            if packet_event.destination_ip in ips:
                return True
        return False

    def should_block(self, raw_packet, packet_event):
        if packet_event.source_port in self.blocked_port_set:
            return True
        if packet_event.destination_port in self.blocked_port_set:
            return True
        if packet_event.application_protocol in self.blocked_protocol_set:
            return True
        if self.is_destination_ip_blocked(packet_event):
            return True
        return False