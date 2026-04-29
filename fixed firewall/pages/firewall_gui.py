import wx
import socket

class FirewallGUI(wx.Panel):
    def __init__(self, parent, policy_client,size):
        super().__init__(parent,size=size)  

        self.policy_client = policy_client
        self.enforcer = policy_client.enforcer
        self.application_protocols = {"FTP", "SMTP", "SMTP", "HTTP", "HTTPS"}

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        font = wx.Font(12, wx.FONTFAMILY_DEFAULT,
                       wx.FONTSTYLE_NORMAL,
                       wx.FONTWEIGHT_BOLD)

        self.port_list = wx.ListBox(self, style=wx.LB_SINGLE)
        self.protocol_list = wx.ListBox(self, style=wx.LB_SINGLE)
        self.domain_list = wx.ListBox(self, style=wx.LB_SINGLE)

        for lb in [self.port_list, self.protocol_list, self.domain_list]:
            lb.SetFont(font)

        add_port = wx.Button(self, label="Add Port")
        rem_port = wx.Button(self, label="Remove Port")
        add_proto = wx.Button(self, label="Add Protocol")
        rem_proto = wx.Button(self, label="Remove Protocol")
        add_dom = wx.Button(self, label="Add Domain")
        rem_dom = wx.Button(self, label="Remove Domain")
        refresh_btn = wx.Button(self, label="Refresh")
        curfew_btn = wx.Button(self, label="enable curfew")


        def make_vbox(title, listbox, add_btn, rem_btn):
            box = wx.BoxSizer(wx.VERTICAL)
            box.Add(wx.StaticText(self, label=title), 0, wx.TOP, 5)
            box.Add(listbox, 1, wx.EXPAND | wx.ALL, 5)
            box.Add(add_btn, 0, wx.EXPAND | wx.ALL, 2)
            box.Add(rem_btn, 0, wx.EXPAND | wx.ALL, 2)
            return box

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(make_vbox("Ports", self.port_list, add_port, rem_port), 1, wx.EXPAND)
        hbox.Add(make_vbox("Protocols", self.protocol_list, add_proto, rem_proto), 1, wx.EXPAND)
        hbox.Add(make_vbox("Domains", self.domain_list, add_dom, rem_dom), 1, wx.EXPAND)

        main_sizer.Add(hbox, 1, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(refresh_btn, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(main_sizer)

        # Bind buttons
        add_port.Bind(wx.EVT_BUTTON, self.add_port)
        rem_port.Bind(wx.EVT_BUTTON, self.remove_port)
        add_proto.Bind(wx.EVT_BUTTON, self.add_protocol)
        rem_proto.Bind(wx.EVT_BUTTON, self.remove_protocol)
        add_dom.Bind(wx.EVT_BUTTON, self.add_domain)
        rem_dom.Bind(wx.EVT_BUTTON, self.remove_domain)
        refresh_btn.Bind(wx.EVT_BUTTON, self.refresh_lists)
        curfew_btn.Bind(wx.EVT_BUTTON, self.send_curfew)
        
    def is_valid_domain(self, domain):
        try:
            socket.gethostbyname(domain)
            return True
        except socket.error:
            return False
            
    def check_admin(self):
        if not self.policy_client.is_admin:
            wx.MessageBox("Only Admin can change rules here!","Control Panel",wx.OK | wx.ICON_WARNING)
            return False
        return True
    
    def send_curfew(self,event):
        if not self.check_admin():
            return
        print("curfew enabled")
        self.policy_client.sock.send(self.policy_client.encrypt("enable_curfew"))
        
    def refresh_lists(self, event=None):
        self.port_list.Set([str(p) for p in self.enforcer.blocked_ports])
        self.protocol_list.Set(list(self.enforcer.blocked_protocols))
        self.domain_list.Set(list(self.enforcer.blocked_domains))

    def add_port(self, event):
        if not self.check_admin():
            return
        dlg = wx.TextEntryDialog(self, "Enter port number:")
        if dlg.ShowModal() == wx.ID_OK:
            try:
                port = int(dlg.GetValue())
                if port < 1 or port > 65535:
                    wx.MessageBox("ERROR: THE PORT REACHED THE LIMIT","PORT ERORR",wx.OK | wx.ICON_WARNING)
                    return 
                current = list(self.enforcer.blocked_ports)
                if port not in current:
                    current.append(port)
                    self.policy_client.command_update_rules({"blocked_ports": current})
            except ValueError:
                pass
        dlg.Destroy()

    def remove_port(self, event):
        if not self.check_admin():
            return
        selection = self.port_list.GetSelection()
        if selection == wx.NOT_FOUND:
            return
        port = int(self.port_list.GetString(selection))
        current = list(self.enforcer.blocked_ports)
        if port in current:
            current.remove(port)
            self.policy_client.command_update_rules({"blocked_ports": current})

    def add_protocol(self, event):
        if not self.check_admin():
            return
        dlg = wx.TextEntryDialog(self, "Enter protocol:")
        if dlg.ShowModal() == wx.ID_OK:
            protocol = dlg.GetValue().strip().upper()
            if not protocol in self.application_protocols:
                wx.MessageBox("PROTOCOL UNAVAILABLE","PROTOCOL ERROR",wx.OK | wx.ICON_WARNING)
                return
            current = list(self.enforcer.blocked_protocols)
            if protocol and protocol not in current:
                current.append(protocol)
                self.policy_client.command_update_rules({"blocked_protocols": current})
        dlg.Destroy()

    def remove_protocol(self, event):
        if not self.check_admin():
            return
        selection = self.protocol_list.GetSelection()
        if selection == wx.NOT_FOUND:
            return
        protocol = self.protocol_list.GetString(selection)
        current = list(self.enforcer.blocked_protocols)
        if protocol in current:
            current.remove(protocol)
            self.policy_client.command_update_rules({"blocked_protocols": current})

    def add_domain(self, event):
        if not self.check_admin():
            return
        dlg = wx.TextEntryDialog(self, "Enter domain:")
        if dlg.ShowModal() == wx.ID_OK:
            domain = dlg.GetValue().strip().lower()
            domain_to_check = "www."+domain
            if not self.is_valid_domain(domain_to_check):
                wx.MessageBox("ERORR: THE DOMAIN DOESNT EXIST!","Domain Error",wx.OK | wx.ICON_WARNING)
                return
            current = list(self.enforcer.blocked_domains)
            if domain and domain not in current:
                current.append(domain)
                self.policy_client.command_update_rules({"blocked_domains": current})
        dlg.Destroy()

    def remove_domain(self, event):
        if not self.check_admin():
            return
        selection = self.domain_list.GetSelection()
        if selection == wx.NOT_FOUND:
            return
        domain = self.domain_list.GetString(selection)
        current = list(self.enforcer.blocked_domains)
        if domain in current:
            current.remove(domain)
            self.policy_client.command_update_rules({"blocked_domains": current})