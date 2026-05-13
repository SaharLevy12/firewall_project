import wx


class homePanel(wx.Panel):
    def __init__(self, parent, size):
        super().__init__(parent, size=size)

        self.parent = parent

        self.SetBackgroundColour("#0f172a")

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.main_sizer.AddStretchSpacer()

        logo = wx.StaticText(self, label="◑")
        logo.SetFont(wx.Font(
            72,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD
        ))
        logo.SetForegroundColour("#c4b5fd")

        self.main_sizer.Add(
            logo,
            0,
            wx.ALIGN_CENTER | wx.BOTTOM,
            10
        )

        self.title = wx.StaticText(
            self,
            label="Welcome to LunarGuard"
        )

        self.title.SetFont(wx.Font(
            30,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD,
            faceName="Segoe UI"
        ))

        self.title.SetForegroundColour("#f8fafc")

        self.main_sizer.Add(
            self.title,
            0,
            wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM,
            10
        )

        subtitle = wx.StaticText(
            self,
            label="Modern encrypted firewall management"
        )

        subtitle.SetFont(wx.Font(
            12,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL,
            faceName="Segoe UI"
        ))

        subtitle.SetForegroundColour("#94a3b8")

        self.main_sizer.Add(
            subtitle,
            0,
            wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM,
            35
        )

        button_panel = wx.Panel(self)
        button_panel.SetBackgroundColour("#1e293b")

        button_sizer = wx.BoxSizer(wx.VERTICAL)

        btn_login = wx.Button(
            button_panel,
            label="Login",
            size=(220, 50)
        )

        btn_register = wx.Button(
            button_panel,
            label="Register",
            size=(220, 50)
        )

        btn_login.SetBackgroundColour("#7c3aed")
        btn_login.SetForegroundColour("#ffffff")
        btn_login.SetWindowStyle(wx.BORDER_NONE)

        btn_register.SetBackgroundColour("#334155")
        btn_register.SetForegroundColour("#ffffff")
        btn_register.SetWindowStyle(wx.BORDER_NONE)

        btn_login.Bind(wx.EVT_BUTTON, self.on_login_click)
        btn_register.Bind(wx.EVT_BUTTON, self.on_register_click)

        btn_login.Bind(
            wx.EVT_ENTER_WINDOW,
            lambda e: btn_login.SetBackgroundColour("#6d28d9")
        )

        btn_login.Bind(
            wx.EVT_LEAVE_WINDOW,
            lambda e: btn_login.SetBackgroundColour("#7c3aed")
        )

        btn_register.Bind(
            wx.EVT_ENTER_WINDOW,
            lambda e: btn_register.SetBackgroundColour("#475569")
        )

        btn_register.Bind(
            wx.EVT_LEAVE_WINDOW,
            lambda e: btn_register.SetBackgroundColour("#334155")
        )

        button_sizer.Add(
            btn_login,
            0,
            wx.BOTTOM,
            15
        )

        button_sizer.Add(
            btn_register,
            0
        )

        button_panel.SetSizer(button_sizer)

        self.main_sizer.Add(
            button_panel,
            0,
            wx.ALIGN_CENTER | wx.ALL,
            20
        )

        footer = wx.StaticText(
            self,
            label="LunarGuard Firewall © 2026"
        )

        footer.SetForegroundColour("#64748b")

        footer.SetFont(wx.Font(
            9,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL
        ))

        self.main_sizer.AddStretchSpacer()

        self.main_sizer.Add(
            footer,
            0,
            wx.ALIGN_CENTER | wx.BOTTOM,
            20
        )

        self.SetSizer(self.main_sizer)
        self.Layout()

    def on_login_click(self, event):
        frame = wx.GetTopLevelParent(self)
        frame.show_panel("login")

    def on_register_click(self, event):
        frame = wx.GetTopLevelParent(self)
        frame.show_panel("reg")