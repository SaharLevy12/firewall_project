import re
import wx

class Utilities:
    def __init__(self):
        pass

    def check_password(password,label):

        label.SetForegroundColour(wx.RED)

        if len(password) < 8:
            label.Label = "Password must be at least 8 characters long."
            return False

        if not re.search(r'[A-Z]', password):
            label.Label = "Password must contain at least one uppercase letter."
            return False

        if not re.search(r'[a-z]', password):
            label.Label = "Password must contain at least one lowercase letter."
            return False

        if not re.search(r'\d', password):
            label.Label = "Password must contain at least one digit."
            return False

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            label.Label = "Password must contain at least one special character."
            return False
        
        label.SetForegroundColour(wx.GREEN)
        label.Label = ""
        return True


    def check_email(email, label):

        label.SetForegroundColour(wx.RED)

        if "@" not in email:
            label.Label = "Email must contain '@'."
            return False

        if email.count("@") > 1:
            label.Label = "Email must contain exactly one @."
            return False

        username, domain = email.split("@")

        if not username:
            label.Label = "Email must have a username before @."
            return False

        if not re.match(r'^[\w\.-]+$', username):
            label.Label = "Username may contain only letters, digits, dots, and hyphens."
            return False

        if domain.lower() != "gmail.com":
            label.Label = "Email must end with @gmail.com"
            return False
        
        label.SetForegroundColour(wx.GREEN)
        label.Label = ""
        return True



    