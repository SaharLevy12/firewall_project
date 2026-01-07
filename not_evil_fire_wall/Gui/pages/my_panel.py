import wx
from Gui.client import Client
from Gui.utilities import Utilities
from Gui.pages.home import homePanel
from Gui.pages.register import regPanel
from Gui.pages.login import loginPanel
from Gui.pages.user import UserPanel  


class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None)
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

class MyFrame(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title="LunarGuard", size=(800,600))
        self.client = Client()
        self.utilities = Utilities()

        self.home = homePanel(self, size=(800,600))
        self.reg = regPanel(self, size=(800,600))
        self.login = loginPanel(self, size=(800,600))

        self.show_panel("home")

    def show_user_panel(self,username):
        size=(800,600)
        self.home.Hide()
        self.reg.Hide()
        self.login.Hide()

        self.user = UserPanel(self, size, username)
        self.user.Show()

    def show_panel(self, panel):
        self.home.Hide()
        self.reg.Hide()
        self.login.Hide()

        if panel == "home":
            self.home.Show()
        elif panel == "reg":
            self.reg.Show()
        elif panel == "login":
            self.login.Show()

        self.Layout()
        self.Refresh()

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()