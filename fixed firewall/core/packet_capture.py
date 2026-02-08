import pydivert
from datetime import datetime
from models.captured_packet import CapturedPacket


class PacketCapture:
    def __init__(self, packet_callback_function):
        self.packet_callback_function = packet_callback_function

    def start_capture(self):
        with pydivert.WinDivert("ip") as divert:
            for packet in divert:

                packet_event = CapturedPacket(
                    timestamp=datetime.now(),
                    direction="OUT" if packet.is_outbound else "IN",
                    source_ip=packet.src_addr,
                    source_port=packet.src_port,
                    destination_ip=packet.dst_addr,
                    destination_port=packet.dst_port,
                    transport_protocol="",
                    application_protocol="",
                    payload_size=len(packet.payload) if packet.payload else 0
                )

                allowed = self.packet_callback_function(packet, packet_event)

                if allowed:
                    try:
                        divert.send(packet)
                    except OSError:
                        continue
