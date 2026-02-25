from core.packet_capture import PacketCapture
from core.firewall_engine import FirewallEngine

def main():
    print("Firewall started – capturing and detecting network packets in real time")
    firewall_engine = FirewallEngine()
    packet_capture = PacketCapture(firewall_engine.process_packet)
    try:
        packet_capture.start_capture()
    except KeyboardInterrupt:
        print("\nFirewall packet capture stopped by user")

if __name__ == "__main__":
    main()
