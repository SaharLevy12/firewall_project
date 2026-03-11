import socket

class Enforcer:
    def __init__(self):
        self.blocked_ports = set()
        self.blocked_protocols = set()
        self.blocked_domains = set()
        self.blocked_domain_ip_cache = {} 

    def resolve_blocked_domains(self):
        self.blocked_domain_ip_cache = {}
        for domain in self.blocked_domains:
            try:
                domain = "www."+domain
                ips = socket.gethostbyname_ex(domain)[2]
                self.blocked_domain_ip_cache[domain] = set(ips)
            except:
                pass

    def update_rules(self, rules):
        self.blocked_ports = set(rules.get("blocked_ports", []))
        self.blocked_protocols = set(rules.get("blocked_protocols", []))
        self.blocked_domains = set(rules.get("blocked_domains", []))
        self.resolve_blocked_domains()

    def is_destination_ip_blocked(self, packet_event):
        for ips in self.blocked_domain_ip_cache.values():
            if packet_event.destination_ip in ips:
                return True
        return False

    def should_block(self, raw_packet, packet_event):
        if packet_event.source_port in self.blocked_ports:
            return True
        if packet_event.destination_port in self.blocked_ports:
            return True
        if packet_event.application_protocol in self.blocked_protocols:
            return True
        if self.is_destination_ip_blocked(packet_event):
            return True
        return False