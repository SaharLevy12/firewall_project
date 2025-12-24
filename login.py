import wx

class loginPanel(wx.Panel):
    def __init__(self, parent, size):
        super().__init__(parent, size=size)
        self.parent = parent
        self.SetBackgroundColour("lightyellow")

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.title = wx.StaticText(self, label="Login")
        self.title.SetFont(wx.Font(24, wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL,
               faceName="Segoe UI"))
        
        self.sizer.Add(self.title, 0, wx.ALIGN_CENTER_HORIZONTAL)

        form_sizer = wx.BoxSizer(wx.VERTICAL)
        form_sizer.Add(wx.StaticText(self, label="Email:"), 0, wx.ALIGN_LEFT)
        self.email = wx.TextCtrl(self,size=(200,25))
        form_sizer.Add(self.email)

        self.error_email = wx.StaticText(self,label="")
        form_sizer.Add(self.error_email,0,wx.ALIGN_CENTER)

        form_sizer.Add(wx.StaticText(self, label="Password:"), 0, wx.ALIGN_LEFT)
        self.password = wx.TextCtrl(self, style=wx.TE_PASSWORD,size=(200,25))
        form_sizer.Add(self.password)

        self.error_password = wx.StaticText(self,label="")
        form_sizer.Add(self.error_password,0,wx.ALIGN_CENTER)

        self.sizer.Add(form_sizer, 0, wx.ALIGN_CENTER, 20)

        btn_sizer = wx.BoxSizer(wx.VERTICAL)

        btn_login = wx.Button(self, label="Login")
        btn_login.Bind(wx.EVT_BUTTON, self.on_click_login)
        btn_sizer.Add(btn_login)

        btn_home = wx.Button(self, label="home")
        btn_home.Bind(wx.EVT_BUTTON, self.on_click_home)
        btn_sizer.Add(btn_home)

        self.sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL)

        self.SetSizer(self.sizer)
        self.Layout()


    def on_click_login(self, event):

        flag = True
        flag = self.parent.utilities.check_email(self.email.GetValue(),self.error_email) and flag
        flag = self.parent.utilities.check_password(self.password.GetValue(),self.error_password) and flag

        if flag:
            public_key = self.parent.client.public_key
            request = f"login,{self.email.GetValue()},{self.password.GetValue()}"
            request = self.parent.utilities.encrypt(request,public_key)
            self.parent.client.send_encrypted_data(request)
            data = self.parent.client.recv_data()
            answer,username = data.split(",")
            if answer == "login successful":    
                self.parent.show_user_panel(username)

    def on_click_home(self,event):
        self.parent.show_panel("home")
