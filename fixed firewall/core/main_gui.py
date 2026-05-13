import wx
from pages.firewall_gui import FirewallGUI
from pages.login import loginPanel
from pages.register import regPanel
from pages.home import homePanel
import json


class MainGUI(wx.Frame):
    def __init__(self, policy_client):
        super().__init__(None, title="LunarGuard Firewall", size=(700, 500))

        self.policy_client = policy_client
        self.policy_client.gui = self

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

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.process_updates, self.timer)
        self.timer.Start(100)

        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        try:
            self.policy_client.disconnect()
        except:
            pass

        self.timer.Stop()
        self.Destroy()

    def show_panel(self, name):
        if name not in self.panels:
            return

        if self.current_panel:
            self.current_panel.Hide()

        self.current_panel = self.panels[name]
        self.current_panel.Show()
        self.panel_container.Layout()

    def rebuild_firewall(self):
        if "firewall" in self.panels:
            self.panels["firewall"].Destroy()
            del self.panels["firewall"]

        self.panels["firewall"] = FirewallGUI(
            self.panel_container,
            self.policy_client,
            size=(700, 500))

        self.sizer.Add(self.panels["firewall"], 1, wx.EXPAND)
        self.panel_container.Layout()

    def show_firewall(self):
        if "firewall" not in self.panels:
            self.rebuild_firewall()

        self.show_panel("firewall")
        self.panels["firewall"].refresh_lists()

    def process_updates(self, event):
        q = self.policy_client.gui_queue

        while not q.empty():
            msg = q.get()

            if msg.startswith("rules"):
                rules = json.loads(msg[len("rules "):])
                self.policy_client.enforcer.update_rules(rules)

                if "firewall" in self.panels:
                    panel = self.panels["firewall"]
                    if panel:
                        panel.refresh_lists()

            elif msg.startswith("login success"):
                _, username, is_admin = msg.split("|")

                self.policy_client.username = username
                self.policy_client.is_admin = (is_admin == "1")

                self.rebuild_firewall()
                self.show_firewall()

            elif msg.startswith("register success"):
                wx.MessageBox("Register success", "Info", wx.OK)