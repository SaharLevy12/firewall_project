import wx
from utilities import Utilities
import tkinter as tk
from tkinter import messagebox


class regPanel(wx.Panel):
    def __init__(self, parent, size):
        super().__init__(parent, size=size)

        self.parent = parent

        self.SetBackgroundColour("#0f172a")

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        top_space = wx.BoxSizer(wx.VERTICAL)

        moon = wx.StaticText(self, label="◑")
        moon.SetFont(wx.Font(
            38,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD
        ))
        moon.SetForegroundColour("#c4b5fd")

        title = wx.StaticText(self, label="LunarGuard Register")
        title.SetFont(wx.Font(
            24,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD,
            faceName="Segoe UI"
        ))
        title.SetForegroundColour("#f8fafc")

        subtitle = wx.StaticText(
            self,
            label="Create a secure firewall account"
        )

        subtitle.SetFont(wx.Font(
            11,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL,
            faceName="Segoe UI"
        ))

        subtitle.SetForegroundColour("#94a3b8")

        top_space.AddSpacer(25)
        top_space.Add(moon, 0, wx.ALIGN_CENTER | wx.BOTTOM, 5)
        top_space.Add(title, 0, wx.ALIGN_CENTER | wx.BOTTOM, 5)
        top_space.Add(subtitle, 0, wx.ALIGN_CENTER | wx.BOTTOM, 20)

        self.main_sizer.Add(top_space, 0, wx.EXPAND)

        card = wx.Panel(self)
        card.SetBackgroundColour("#1e293b")

        card_sizer = wx.BoxSizer(wx.VERTICAL)

        username_text = wx.StaticText(card, label="Username")
        username_text.SetForegroundColour("#e2e8f0")

        username_text.SetFont(wx.Font(
            10,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD
        ))

        self.username = wx.TextCtrl(
            card,
            size=(260, 35)
        )

        self.username.SetBackgroundColour("#334155")
        self.username.SetForegroundColour("#f8fafc")

        email_text = wx.StaticText(card, label="Email")
        email_text.SetForegroundColour("#e2e8f0")

        email_text.SetFont(wx.Font(
            10,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD
        ))

        self.email = wx.TextCtrl(
            card,
            size=(260, 35)
        )

        self.email.SetBackgroundColour("#334155")
        self.email.SetForegroundColour("#f8fafc")

        self.error_email = wx.StaticText(card, label="")
        self.error_email.SetForegroundColour("#f87171")

        password_text = wx.StaticText(card, label="Password")
        password_text.SetForegroundColour("#e2e8f0")

        password_text.SetFont(wx.Font(
            10,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD
        ))

        self.password = wx.TextCtrl(
            card,
            style=wx.TE_PASSWORD,
            size=(260, 35)
        )

        self.password.SetBackgroundColour("#334155")
        self.password.SetForegroundColour("#f8fafc")

        self.error_password = wx.StaticText(card, label="")
        self.error_password.SetForegroundColour("#f87171")

        register_btn = wx.Button(
            card,
            label="Register",
            size=(260, 42)
        )

        register_btn.SetBackgroundColour("#7c3aed")
        register_btn.SetForegroundColour("#ffffff")
        register_btn.SetWindowStyle(wx.BORDER_NONE)

        home_btn = wx.Button(
            card,
            label="Back Home",
            size=(260, 42)
        )

        home_btn.SetBackgroundColour("#334155")
        home_btn.SetForegroundColour("#ffffff")
        home_btn.SetWindowStyle(wx.BORDER_NONE)

        register_btn.Bind(wx.EVT_BUTTON, self.on_click_reg)
        home_btn.Bind(wx.EVT_BUTTON, self.on_click_home)

        register_btn.Bind(wx.EVT_ENTER_WINDOW,
                          lambda e: register_btn.SetBackgroundColour("#6d28d9"))

        register_btn.Bind(wx.EVT_LEAVE_WINDOW,
                          lambda e: register_btn.SetBackgroundColour("#7c3aed"))

        home_btn.Bind(wx.EVT_ENTER_WINDOW,
                      lambda e: home_btn.SetBackgroundColour("#475569"))

        home_btn.Bind(wx.EVT_LEAVE_WINDOW,
                      lambda e: home_btn.SetBackgroundColour("#334155"))

        card_sizer.Add(username_text, 0, wx.BOTTOM, 6)
        card_sizer.Add(self.username, 0, wx.BOTTOM, 15)

        card_sizer.Add(email_text, 0, wx.BOTTOM, 6)
        card_sizer.Add(self.email, 0, wx.BOTTOM, 5)
        card_sizer.Add(self.error_email, 0, wx.BOTTOM, 12)

        card_sizer.Add(password_text, 0, wx.BOTTOM, 6)
        card_sizer.Add(self.password, 0, wx.BOTTOM, 5)
        card_sizer.Add(self.error_password, 0, wx.BOTTOM, 18)

        card_sizer.Add(register_btn, 0, wx.BOTTOM, 12)
        card_sizer.Add(home_btn, 0)

        card.SetSizer(card_sizer)

        wrapper = wx.BoxSizer(wx.HORIZONTAL)

        wrapper.AddStretchSpacer()
        wrapper.Add(card, 0, wx.ALL, 25)
        wrapper.AddStretchSpacer()

        self.main_sizer.Add(wrapper, 1, wx.ALIGN_CENTER)

        self.SetSizer(self.main_sizer)
        self.Layout()

    def on_click_reg(self, event):

        flag = True
        flag = Utilities.check_email(
            self.email.GetValue(),
            self.error_email
        ) and flag

        flag = Utilities.check_password(
            self.password.GetValue(),
            self.error_password
        ) and flag

        if flag:
            parent = wx.GetTopLevelParent(self)

            request = (
                f"register,"
                f"{self.username.GetValue()},"
                f"{self.email.GetValue()},"
                f"{self.password.GetValue()}"
            )

            request = parent.policy_client.encrypt(request)
            
            self.username.Label = ""
            self.email.Label = ""
            self.error_email.Label = ""
            self.password.Label = ""
            self.error_password.Label = ""

            parent.policy_client.sock.send(request)

    def on_click_home(self, event):
        frame = wx.GetTopLevelParent(self)
        frame.show_panel("home")