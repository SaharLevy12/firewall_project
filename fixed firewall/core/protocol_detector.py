class ProtocolDetector:
    APPLICATION_PORTS = {21: "FTP", 25: "SMTP", 587: "SMTP", 80: "HTTP", 443: "HTTPS"}

    def detect_transport_protocol(self, packet) -> str:
        if packet.tcp:
            return "TCP"
        if packet.udp:
            return "UDP"
        return "OTHER"

    def detect_application_protocol(self, source_port: int | None, destination_port: int | None) -> str:
        for port in (source_port, destination_port):
            if port in self.APPLICATION_PORTS:
                return self.APPLICATION_PORTS[port]
        return "UNKNOWN"
