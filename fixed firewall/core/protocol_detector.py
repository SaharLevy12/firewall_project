class ProtocolDetector:
    APPLICATION_PORTS = {21: "FTP", 25: "SMTP", 587: "SMTP", 465 : "SMTP" , 993: "POP3" , 80: "HTTP", 443: "HTTPS"}

    def detect_transport_protocol(self, packet):
        if packet.tcp:
            return "TCP"
        if packet.udp:
            return "UDP"
        return "OTHER"

    def detect_application_protocol(self, source_port, destination_port):
        for port in (source_port, destination_port):
            if port in self.APPLICATION_PORTS:
                return self.APPLICATION_PORTS[port]
        return "UNKNOWN"
