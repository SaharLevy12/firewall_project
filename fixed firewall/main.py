import threading
import wx
from core.packet_capture import PacketCapture
from core.firewall_engine import FirewallEngine
from core.policy_client import PolicyClient
from core.main_gui import MainGUI

def main():
    firewall = FirewallEngine()
    user = PolicyClient(firewall.enforcer)
    user.connect()

    app = wx.App()
    frame = MainGUI(user)
    user.gui = frame
    frame.Show()

    capture = PacketCapture(firewall.process_packet)
    threading.Thread(target=capture.start_capture, daemon=True).start()

    app.MainLoop()

if __name__=="__main__":
    main()