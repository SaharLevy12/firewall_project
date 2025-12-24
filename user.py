import wx

class UserPanel(wx.Panel):
    def __init__(self, parent, size, username):
        super().__init__(parent, size=size)
        self.parent = parent
        self.SetBackgroundColour("lightblue")

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.title = wx.StaticText(self, label=f"Welcome to LunarGuard {username}")
        self.title.SetFont(wx.Font(24, wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL,
               faceName="Segoe UI"))

        