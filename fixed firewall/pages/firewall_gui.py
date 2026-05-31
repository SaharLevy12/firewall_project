import wx
import socket


class FirewallGUI(wx.Panel):
    def __init__(self, parent, policy_client, size):
        super().__init__(parent, size=size)

        self.policy_client = policy_client
        self.enforcer = policy_client.enforcer
        self.is_admin = policy_client.is_admin

        self.application_protocols = {"FTP", "SMTP", "HTTP", "HTTPS"}

        self.SetBackgroundColour(wx.Colour(15, 23, 42))

        if self.is_admin:
            self.build_admin_ui()
        else:
            self.build_client_ui()

    def style_button(self, button):
        button.SetMinSize((140, 38))

        normal_bg = wx.Colour(88, 101, 242)
        hover_bg = wx.Colour(70, 82, 210)

        button.SetBackgroundColour(normal_bg)
        button.SetForegroundColour(wx.WHITE)

        font = wx.Font(
            10,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD,
            faceName="Segoe UI"
        )

        button.SetFont(font)

        def on_enter(event):
            button.SetBackgroundColour(hover_bg)
            button.SetForegroundColour(wx.WHITE)
            button.Refresh()
            event.Skip()

        def on_leave(event):
            button.SetBackgroundColour(normal_bg)
            button.SetForegroundColour(wx.WHITE)
            button.Refresh()
            event.Skip()

        button.Bind(wx.EVT_ENTER_WINDOW, on_enter)
        button.Bind(wx.EVT_LEAVE_WINDOW, on_leave)

    def create_title(self, text):
        title = wx.StaticText(self, label=text)
        title.SetForegroundColour(wx.WHITE)

        title.SetFont(wx.Font(
            20,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD,
            faceName="Segoe UI"
        ))

        return title

    def create_subtitle(self, text):
        subtitle = wx.StaticText(self, label=text)
        subtitle.SetForegroundColour(wx.Colour(180, 190, 220))

        subtitle.SetFont(wx.Font(
            10,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL,
            faceName="Segoe UI"
        ))

        return subtitle

    def create_logo(self):
        moon = wx.StaticText(self, label="☾")
        moon.SetForegroundColour(wx.Colour(200, 210, 255))

        moon.SetFont(wx.Font(
            38,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD
        ))

        return moon

    def style_listbox(self, listbox):
        listbox.SetBackgroundColour(wx.Colour(30, 41, 59))
        listbox.SetForegroundColour(wx.WHITE)

        listbox.SetFont(wx.Font(
            10,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL,
            faceName="Segoe UI"
        ))

    def build_admin_ui(self):
        main = wx.BoxSizer(wx.VERTICAL)

        header = wx.BoxSizer(wx.VERTICAL)

        logo = self.create_logo()
        title = self.create_title("Admin Firewall Control Panel")
        subtitle = self.create_subtitle("Manage network rules and active protection")

        header.Add(logo, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        header.Add(title, 0, wx.ALIGN_CENTER | wx.TOP, 5)
        header.Add(subtitle, 0, wx.ALIGN_CENTER | wx.BOTTOM, 15)

        main.Add(header, 0, wx.EXPAND)

        self.port_in = wx.ListBox(self)
        self.port_out = wx.ListBox(self)
        self.proto_in = wx.ListBox(self)
        self.proto_out = wx.ListBox(self)
        self.domain_list = wx.ListBox(self)

        self.style_listbox(self.port_in)
        self.style_listbox(self.port_out)
        self.style_listbox(self.proto_in)
        self.style_listbox(self.proto_out)
        self.style_listbox(self.domain_list)

        main.Add(
            self.create_admin_card(
                "Ports",
                self.port_in,
                self.port_out,
                self.add_port_in,
                self.add_port_out,
                self.remove_port_in,
                self.remove_port_out
            ),
            1,
            wx.EXPAND | wx.ALL,
            10
        )

        main.Add(
            self.create_admin_card(
                "Protocols",
                self.proto_in,
                self.proto_out,
                self.add_proto_in,
                self.add_proto_out,
                self.remove_proto_in,
                self.remove_proto_out
            ),
            1,
            wx.EXPAND | wx.ALL,
            10
        )

        domain_box = wx.StaticBox(self, label="Domains")
        domain_box.SetForegroundColour(wx.WHITE)

        domain_sizer = wx.StaticBoxSizer(domain_box, wx.VERTICAL)

        domain_sizer.Add(self.domain_list, 1, wx.EXPAND | wx.ALL, 8)

        add_dom = wx.Button(self, label="Add Domain")
        rem_dom = wx.Button(self, label="Remove Domain")

        self.style_button(add_dom)
        self.style_button(rem_dom)

        add_dom.Bind(wx.EVT_BUTTON, self.add_domain)
        rem_dom.Bind(wx.EVT_BUTTON, self.remove_domain)

        btn_row = wx.BoxSizer(wx.HORIZONTAL)
        btn_row.Add(add_dom, 1, wx.RIGHT, 5)
        btn_row.Add(rem_dom, 1)

        domain_sizer.Add(btn_row, 0, wx.EXPAND | wx.ALL, 5)

        main.Add(domain_sizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        refresh_btn = wx.Button(self, label="Refresh")
        curfew_btn = wx.Button(self, label="Enable Curfew")
        logout_btn = wx.Button(self, label="Logout")

        self.style_button(refresh_btn)
        self.style_button(curfew_btn)
        self.style_button(logout_btn)

        refresh_btn.Bind(wx.EVT_BUTTON, self.refresh_lists)
        curfew_btn.Bind(wx.EVT_BUTTON, self.send_curfew)
        logout_btn.Bind(wx.EVT_BUTTON, self.logout)

        action_row = wx.BoxSizer(wx.HORIZONTAL)

        action_row.Add(refresh_btn, 1, wx.RIGHT, 5)
        action_row.Add(curfew_btn, 1, wx.RIGHT, 5)
        action_row.Add(logout_btn, 1)

        main.Add(action_row, 0, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(main)

    def build_client_ui(self):
        main = wx.BoxSizer(wx.VERTICAL)

        header = wx.BoxSizer(wx.VERTICAL)

        logo = self.create_logo()
        title = self.create_title("Firewall Dashboard")
        subtitle = self.create_subtitle("Viewing active protection rules")

        header.Add(logo, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        header.Add(title, 0, wx.ALIGN_CENTER | wx.TOP, 5)
        header.Add(subtitle, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)

        main.Add(header, 0, wx.EXPAND)

        self.summary_text = wx.StaticText(self, label="")
        self.summary_text.SetForegroundColour(wx.WHITE)

        self.summary_text.SetFont(wx.Font(
            10,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD,
            faceName="Segoe UI"
        ))

        main.Add(self.summary_text, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)

        self.port_in = wx.ListBox(self)
        self.port_out = wx.ListBox(self)
        self.proto_in = wx.ListBox(self)
        self.proto_out = wx.ListBox(self)
        self.domain_list = wx.ListBox(self)

        self.style_listbox(self.port_in)
        self.style_listbox(self.port_out)
        self.style_listbox(self.proto_in)
        self.style_listbox(self.proto_out)
        self.style_listbox(self.domain_list)

        main.Add(
            self.create_view_card("Ports", self.port_in, self.port_out),
            1,
            wx.EXPAND | wx.ALL,
            10
        )

        main.Add(
            self.create_view_card("Protocols", self.proto_in, self.proto_out),
            1,
            wx.EXPAND | wx.ALL,
            10
        )

        domain_box = wx.StaticBox(self, label="Domains")
        domain_box.SetForegroundColour(wx.WHITE)

        domain_sizer = wx.StaticBoxSizer(domain_box, wx.VERTICAL)

        domain_sizer.Add(self.domain_list, 1, wx.EXPAND | wx.ALL, 8)

        main.Add(domain_sizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        refresh_btn = wx.Button(self, label="Refresh")
        logout_btn = wx.Button(self, label="Logout")

        self.style_button(refresh_btn)
        self.style_button(logout_btn)

        refresh_btn.Bind(wx.EVT_BUTTON, self.refresh_lists)
        logout_btn.Bind(wx.EVT_BUTTON, self.logout)

        action_row = wx.BoxSizer(wx.HORIZONTAL)

        action_row.Add(refresh_btn, 1, wx.RIGHT, 5)
        action_row.Add(logout_btn, 1)

        main.Add(action_row, 0, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(main)

    def create_admin_card(
        self,
        title,
        list_in,
        list_out,
        add_in,
        add_out,
        rem_in,
        rem_out
    ):
        box = wx.StaticBox(self, label=title)
        box.SetForegroundColour(wx.WHITE)

        sizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)

        in_box = wx.BoxSizer(wx.VERTICAL)

        in_title = wx.StaticText(self, label="IN")
        in_title.SetForegroundColour(wx.WHITE)

        in_box.Add(in_title, 0, wx.ALL, 5)
        in_box.Add(list_in, 1, wx.EXPAND | wx.ALL, 5)

        btn_add_in = wx.Button(self, label="Add IN")
        btn_rem_in = wx.Button(self, label="Remove IN")

        self.style_button(btn_add_in)
        self.style_button(btn_rem_in)

        btn_add_in.Bind(wx.EVT_BUTTON, add_in)
        btn_rem_in.Bind(wx.EVT_BUTTON, rem_in)

        in_box.Add(btn_add_in, 0, wx.EXPAND | wx.ALL, 2)
        in_box.Add(btn_rem_in, 0, wx.EXPAND | wx.ALL, 2)

        out_box = wx.BoxSizer(wx.VERTICAL)

        out_title = wx.StaticText(self, label="OUT")
        out_title.SetForegroundColour(wx.WHITE)

        out_box.Add(out_title, 0, wx.ALL, 5)
        out_box.Add(list_out, 1, wx.EXPAND | wx.ALL, 5)

        btn_add_out = wx.Button(self, label="Add OUT")
        btn_rem_out = wx.Button(self, label="Remove OUT")

        self.style_button(btn_add_out)
        self.style_button(btn_rem_out)

        btn_add_out.Bind(wx.EVT_BUTTON, add_out)
        btn_rem_out.Bind(wx.EVT_BUTTON, rem_out)

        out_box.Add(btn_add_out, 0, wx.EXPAND | wx.ALL, 2)
        out_box.Add(btn_rem_out, 0, wx.EXPAND | wx.ALL, 2)

        sizer.Add(in_box, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(out_box, 1, wx.EXPAND | wx.ALL, 5)

        return sizer

    def create_view_card(self, title, list_in, list_out):
        box = wx.StaticBox(self, label=title)
        box.SetForegroundColour(wx.WHITE)

        sizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)

        in_box = wx.BoxSizer(wx.VERTICAL)

        in_title = wx.StaticText(self, label="Incoming")
        in_title.SetForegroundColour(wx.WHITE)

        in_box.Add(in_title, 0, wx.ALL, 5)
        in_box.Add(list_in, 1, wx.EXPAND | wx.ALL, 5)

        out_box = wx.BoxSizer(wx.VERTICAL)

        out_title = wx.StaticText(self, label="Outgoing")
        out_title.SetForegroundColour(wx.WHITE)

        out_box.Add(out_title, 0, wx.ALL, 5)
        out_box.Add(list_out, 1, wx.EXPAND | wx.ALL, 5)

        sizer.Add(in_box, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(out_box, 1, wx.EXPAND | wx.ALL, 5)

        return sizer

    def refresh_lists(self, event=None):
        self.port_in.Set([str(p) for p in self.enforcer.blocked_ports_in])
        self.port_out.Set([str(p) for p in self.enforcer.blocked_ports_out])

        self.proto_in.Set(list(self.enforcer.blocked_protocols_in))
        self.proto_out.Set(list(self.enforcer.blocked_protocols_out))

        self.domain_list.Set(list(self.enforcer.blocked_domains))

        if not self.is_admin:
            summary = (
                f"Ports: {len(self.enforcer.blocked_ports_in)} IN / "
                f"{len(self.enforcer.blocked_ports_out)} OUT | "
                f"Protocols: {len(self.enforcer.blocked_protocols_in)} IN / "
                f"{len(self.enforcer.blocked_protocols_out)} OUT | "
                f"Domains: {len(self.enforcer.blocked_domains)}"
            )

            self.summary_text.SetLabel(summary)

    def send_curfew(self, event):
        self.policy_client.sock.send(
            self.policy_client.encrypt("enable_curfew")
        )

    def logout(self, event):
        self.policy_client.sock.send(
            self.policy_client.encrypt("logout")
        )

        self.policy_client.gui = None
        self.policy_client.username = None
        self.policy_client.is_admin = False
        self.policy_client.thread = None

        frame = wx.GetTopLevelParent(self)
        frame.show_panel("home")

    def add_port_in(self, e):
        self.add_port("blocked_ports_in")

    def add_port_out(self, e):
        self.add_port("blocked_ports_out")

    def add_port(self, key):
        dlg = wx.TextEntryDialog(self, "Enter port:")

        if dlg.ShowModal() == wx.ID_OK:
            try:
                port = int(dlg.GetValue())

                current = list(getattr(self.enforcer, key))

                if port not in current:
                    current.append(port)

                    self.policy_client.command_update_rules({
                        key: current
                    })

            except:
                pass

        dlg.Destroy()

    def remove_port_in(self, e):
        self.remove_port("blocked_ports_in", self.port_in)

    def remove_port_out(self, e):
        self.remove_port("blocked_ports_out", self.port_out)

    def remove_port(self, key, listbox):
        sel = listbox.GetSelection()

        if sel == wx.NOT_FOUND:
            return

        port = int(listbox.GetString(sel))

        current = list(getattr(self.enforcer, key))

        if port in current:
            current.remove(port)

            self.policy_client.command_update_rules({
                key: current
            })

    def add_proto_in(self, e):
        self.add_proto("blocked_protocols_in")

    def add_proto_out(self, e):
        self.add_proto("blocked_protocols_out")

    def add_proto(self, key):
        dlg = wx.TextEntryDialog(self, "Enter protocol:")

        if dlg.ShowModal() == wx.ID_OK:
            proto = dlg.GetValue().strip().upper()

            if proto not in self.application_protocols:
                wx.MessageBox("Invalid protocol")
                return

            current = list(getattr(self.enforcer, key))

            if proto not in current:
                current.append(proto)

                self.policy_client.command_update_rules({
                    key: current
                })

        dlg.Destroy()

    def remove_proto_in(self, e):
        self.remove_proto("blocked_protocols_in", self.proto_in)

    def remove_proto_out(self, e):
        self.remove_proto("blocked_protocols_out", self.proto_out)

    def remove_proto(self, key, listbox):
        sel = listbox.GetSelection()

        if sel == wx.NOT_FOUND:
            return

        proto = listbox.GetString(sel)

        current = list(getattr(self.enforcer, key))

        if proto in current:
            current.remove(proto)

            self.policy_client.command_update_rules({
                key: current
            })

    def add_domain(self, e):
        dlg = wx.TextEntryDialog(self, "Enter domain:")

        if dlg.ShowModal() == wx.ID_OK:
            domain = dlg.GetValue().strip().lower()

            current = list(self.enforcer.blocked_domains)

            if domain not in current:
                current.append(domain)

                self.policy_client.command_update_rules({
                    "blocked_domains": current
                })

        dlg.Destroy()

    def remove_domain(self, e):
        sel = self.domain_list.GetSelection()

        if sel == wx.NOT_FOUND:
            return

        domain = self.domain_list.GetString(sel)

        current = list(self.enforcer.blocked_domains)

        if domain in current:
            current.remove(domain)

            self.policy_client.command_update_rules({
                "blocked_domains": current
            })