from dataclasses import dataclass
from datetime import datetime

@dataclass
class CapturedPacket:
    timestamp: datetime
    direction: str
    source_ip: str
    source_port: int | None
    destination_ip: str
    destination_port: int | None
    transport_protocol: str
    application_protocol: str
    # payload_size: int
