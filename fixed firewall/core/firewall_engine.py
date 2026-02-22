from core.protocol_detector import ProtocolDetector
from core.logger import Logger
from core.enforcer import Enforcer


class FirewallEngine:
    def __init__(self, config_file):
        self.protocol_detector = ProtocolDetector()
        self.logger = Logger()
        self.enforcer = Enforcer(config_file)

    def process_packet(self, raw_packet, packet_event):
        packet_event.transport_protocol = self.protocol_detector.detect_transport_protocol(raw_packet)
        packet_event.application_protocol = self.protocol_detector.detect_application_protocol(
            packet_event.source_port,
            packet_event.destination_port
        )

        should_block = self.enforcer.should_block(raw_packet, packet_event)

        if should_block:
            self.logger.log_event(packet_event)

        return not should_block