import wx

class homePanel(wx.Panel):
    def __init__(self, parent, size):
        super().__init__(parent, size=size)
        self.parent = parent
        self.SetBackgroundColour("lightblue")

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.title = wx.StaticText(self, label="Welcome to LunarGuard")
        self.title.SetFont(wx.Font(24, wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL,
               faceName="Segoe UI"))
        
        self.sizer.Add(self.title, 0, wx.ALIGN_CENTER_HORIZONTAL)

        btn_sizer = wx.BoxSizer(wx.VERTICAL)
        btn_login = wx.Button(self, label="Login",size=(130,50))
        btn_login.Bind(wx.EVT_BUTTON, self.on_login_click)
        btn_sizer.Add(btn_login, 0, wx.ALL, 10)
        btn_register = wx.Button(self, label="Register",size=(130,50))
        btn_register.Bind(wx.EVT_BUTTON, self.on_register_click)
        btn_sizer.Add(btn_register, 0, wx.ALL, 10)

        self.sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER)
        self.SetSizer(self.sizer)
        self.Layout()

    def on_login_click(self, event):
        frame = wx.GetTopLevelParent(self)
        frame.show_panel("login")

    def on_register_click(self, event):
        frame = wx.GetTopLevelParent(self)
        frame.show_panel("reg")

