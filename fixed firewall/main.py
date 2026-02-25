import threading
import wx
from core.packet_capture import PacketCapture
from core.firewall_engine import FirewallEngine
from core.policy_client import PolicyClient
from core.gui import FirewallGUI

def main():
    firewall = FirewallEngine()
    pc = PolicyClient(firewall.enforcer, username="admin", is_admin=True)

    app = wx.App(False)
    frame = FirewallGUI(pc)
    frame.Show()

    threading.Thread(target=pc.connect, daemon=True).start()

    capture = PacketCapture(firewall.process_packet)
    threading.Thread(target=capture.start_capture, daemon=True).start()

    app.MainLoop()

if __name__=="__main__":
    main()