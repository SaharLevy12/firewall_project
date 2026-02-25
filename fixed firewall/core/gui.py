
import wx
from core.policy_client import PolicyClient

class FirewallGUI(wx.Frame):
    def __init__(self, pc: PolicyClient):
        super().__init__(None, title="Firewall Manager", size=(600,450))
        self.pc = pc
        self.enforcer = pc.enforcer

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        # רשימות
        self.port_list = wx.ListBox(panel, style=wx.LB_SINGLE)
        self.protocol_list = wx.ListBox(panel, style=wx.LB_SINGLE)
        self.domain_list = wx.ListBox(panel, style=wx.LB_SINGLE)
        for lb in [self.port_list, self.protocol_list, self.domain_list]:
            lb.SetFont(font)

        # כפתורים
        add_port = wx.Button(panel, label="Add Port")
        rem_port = wx.Button(panel, label="Remove Port")
        add_proto = wx.Button(panel, label="Add Protocol")
        rem_proto = wx.Button(panel, label="Remove Protocol")
        add_dom = wx.Button(panel, label="Add Domain")
        rem_dom = wx.Button(panel, label="Remove Domain")
        refresh = wx.Button(panel, label="Refresh")

        # סידור
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        def make_vbox(label, lb, add_btn, rem_btn):
            vb = wx.BoxSizer(wx.VERTICAL)
            vb.Add(wx.StaticText(panel,label=label),0,wx.TOP,5)
            vb.Add(lb,1,wx.EXPAND|wx.ALL,5)
            vb.Add(add_btn,0,wx.EXPAND|wx.ALL,2)
            vb.Add(rem_btn,0,wx.EXPAND|wx.ALL,2)
            return vb
        hbox.Add(make_vbox("Ports",self.port_list,add_port,rem_port),1,wx.EXPAND)
        hbox.Add(make_vbox("Protocols",self.protocol_list,add_proto,rem_proto),1,wx.EXPAND)
        hbox.Add(make_vbox("Domains",self.domain_list,add_dom,rem_dom),1,wx.EXPAND)
        sizer.Add(hbox,1,wx.EXPAND|wx.ALL,5)
        sizer.Add(refresh,0,wx.EXPAND|wx.ALL,5)
        panel.SetSizer(sizer)

        # Bind
        add_port.Bind(wx.EVT_BUTTON,self.add_port)
        rem_port.Bind(wx.EVT_BUTTON,self.remove_port)
        add_proto.Bind(wx.EVT_BUTTON,self.add_protocol)
        rem_proto.Bind(wx.EVT_BUTTON,self.remove_protocol)
        add_dom.Bind(wx.EVT_BUTTON,self.add_domain)
        rem_dom.Bind(wx.EVT_BUTTON,self.remove_domain)
        refresh.Bind(wx.EVT_BUTTON,self.refresh_lists)

        self.refresh_lists()
        self.pc.gui = self

    def refresh_lists(self,event=None):
        self.port_list.Set(list(map(str,sorted(self.enforcer.blocked_port_set))))
        self.protocol_list.Set(sorted(self.enforcer.blocked_protocol_set))
        self.domain_list.Set(sorted(self.enforcer.blocked_domain_set))

    def add_port(self,event): self._add_item("blocked_ports", self.port_list, int)
    def remove_port(self,event): self._remove_item("blocked_ports", self.port_list, int)
    def add_protocol(self,event): self._add_item("blocked_protocols", self.protocol_list, str, True)
    def remove_protocol(self,event): self._remove_item("blocked_protocols", self.protocol_list, str)
    def add_domain(self,event): self._add_item("blocked_domains", self.domain_list, str)
    def remove_domain(self,event): self._remove_item("blocked_domains", self.domain_list, str)

    def _add_item(self, rule_attr, lb, cast=str, upper=False):
        if not self.pc.is_admin: return
        dlg = wx.TextEntryDialog(self,f"Enter value:")
        if dlg.ShowModal()==wx.ID_OK:
            try:
                val = cast(dlg.GetValue())
                if upper: val = str(val).upper()
                current = list(getattr(self.enforcer, rule_attr))
                if val not in current:
                    current.append(val)
                    self.pc.update_rules({rule_attr: current})
            except:
                pass
        dlg.Destroy()
        self.refresh_lists()

    def _remove_item(self, rule_attr, lb, cast=str):
        if not self.pc.is_admin: return
        sel = lb.GetSelection()
        if sel!=wx.NOT_FOUND:
            val = cast(lb.GetString(sel))
            current = list(getattr(self.enforcer, rule_attr))
            if val in current:
                current.remove(val)
                self.pc.update_rules({rule_attr: current})
        self.refresh_lists()