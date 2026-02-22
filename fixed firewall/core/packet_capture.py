import pydivert
from datetime import datetime
from models.captured_packet import CapturedPacket


class PacketCapture:
    def __init__(self, packet_callback_function):
        self.packet_callback_function = packet_callback_function

    def start_capture(self):
        with pydivert.WinDivert("tcp or udp") as divert:
            for raw_packet in divert:

                packet_event = CapturedPacket(
                    timestamp=datetime.now(),
                    direction="OUT" if raw_packet.is_outbound else "IN",
                    source_ip=raw_packet.src_addr,
                    source_port=raw_packet.src_port,
                    destination_ip=raw_packet.dst_addr,
                    destination_port=raw_packet.dst_port,
                    transport_protocol="",
                    application_protocol="",
                    # payload_size=len(raw_packet.payload) if raw_packet.payload else 0
                )

                allowed = self.packet_callback_function(raw_packet, packet_event)

                if allowed:
                    try:
                        divert.send(raw_packet)
                    except OSError:
                        continue