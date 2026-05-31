import socket
import os
from datetime import datetime

class Enforcer:
    def __init__(self):
        self.blocked_ports_in = set()
        self.blocked_ports_out = set()

        self.blocked_protocols_in = set()
        self.blocked_protocols_out = set()

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
        print("updating rules..")
        self.blocked_ports_in = set(rules["blocked_ports_in"])
        self.blocked_ports_out = set(rules["blocked_ports_out"])

        self.blocked_protocols_in = set(rules["blocked_protocols_in"])
        self.blocked_protocols_out = set(rules["blocked_protocols_out"])

        self.blocked_domains = set(rules["blocked_domains"])

        self.resolve_blocked_domains()
        print(rules)

        print(self.blocked_ports_in)
        print(self.blocked_ports_out)
        print(self.blocked_protocols_in)
        print(self.blocked_protocols_out)
        print(self.blocked_domains)



    def is_destination_ip_blocked(self, packet_event):
        for ips in self.blocked_domain_ip_cache.values():
            if packet_event.destination_ip in ips:
                return True
        return False
    
    def enable_curfew(self,sock):
        try:
            print("shutdowning...")
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
            # os.system("shutdown /s /t 0")
        except socket.error as e:
            print(f"Error: {e}")
        

    def should_block(self, raw_packet, packet_event):
        #print(rules)

        print(self.blocked_ports_in)
        print(self.blocked_ports_out)
        print(self.blocked_protocols_in)
        print(self.blocked_protocols_out)
        print(self.blocked_domains)

        direction = packet_event.direction

        if direction == "OUT":
            # print(1,packet_event.destination_port,self.blocked_ports_out)
            if packet_event.destination_port in self.blocked_ports_out:
                return True
        else:  
            # print(2,packet_event.source_port,self.blocked_ports_in)
            if packet_event.source_port in self.blocked_ports_in:
                return True

        if direction == "OUT":
            # print(3,packet_event.application_protocol,self.blocked_protocols_out)
            if packet_event.application_protocol in self.blocked_protocols_out:
                return True
        else:
            # print(4,packet_event.application_protocol,self.blocked_protocols_in)
            if packet_event.application_protocol in self.blocked_protocols_in:
                return True

        if self.is_destination_ip_blocked(packet_event):
            return True

        return False