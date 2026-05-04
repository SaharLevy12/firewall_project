import wx
from pages.firewall_gui import FirewallGUI
from pages.login import loginPanel
from pages.register import regPanel
from pages.home import homePanel


class MainGUI(wx.Frame):
    def __init__(self, policy_client):
        super().__init__(None, title="LunarGuard Firewall", size=(700, 500))

        self.policy_client = policy_client

        self.panel_container = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel_container.SetSizer(self.sizer)

        self.panels = {}

        self.panels["home"] = homePanel(self.panel_container, size=(700, 500))
        self.panels["login"] = loginPanel(self.panel_container, size=(700, 500))
        self.panels["reg"] = regPanel(self.panel_container, size=(700, 500))

        for p in self.panels.values():
            p.Hide()
            self.sizer.Add(p, 1, wx.EXPAND)

        self.current_panel = None
        self.show_panel("home")

    def show_panel(self, name):
        if self.current_panel:
            self.current_panel.Hide()

        self.current_panel = self.panels[name]
        self.current_panel.Show()
        self.panel_container.Layout()


    def rebuild_firewall(self):
        if "firewall" in self.panels:
            self.panels["firewall"].Destroy()

        from pages.firewall_gui import FirewallGUI

        self.panels["firewall"] = FirewallGUI(
            self.panel_container,
            self.policy_client,
            size=(700, 500)
        )

        self.sizer.Add(self.panels["firewall"], 1, wx.EXPAND)

    def show_firewall(self):
        self.show_panel("firewall")
        self.panels["firewall"].refresh_lists()