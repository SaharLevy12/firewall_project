import re
import wx
import google.genai as genai
from core.protocol_detector import ProtocolDetector
import os

class Utilities:
    def __init__(self):
        self.protocol_detector = ProtocolDetector()


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
            label.Label = "Email must end with @gmail.com."
            return False
        
        label.SetForegroundColour(wx.GREEN)
        label.Label = ""
        return True
    

    # def ask_ai_opinion(self, raw_packet, packet_event):
    #     packet_event.transport_protocol = self.protocol_detector.detect_transport_protocol(raw_packet)
    #     packet_event.application_protocol = self.protocol_detector.detect_application_protocol(
    #     packet_event.source_port, packet_event.destination_port)

    #     API_KEY = os.getenv("MASTER_KEY")

    #     client = genai.Client(api_key=API_KEY)

    #     request = f"""you are now an expert firewall enforcer i will give you a packet that tries to go through my firewall after passing the port and domains rules
    #                 and now your job is to inspect by the aspect of the packet i will give and rate the danger level of the packet when 1 is the safest and 10 is the most dangerous
    #                 if the rating is 5 or more you should give me a sign to block the packet by writing True - for packet that is valid and False - invalid packet 
    #                 make sure True or False is the first word of the answer and after it there is comma -> , so i can split the text and get True or False
    #                 the aspect are: 1 - direction - in/out
    #                 2 - source ip
    #                 3 - source port
    #                 4 - destination ip
    #                 5 - destination port
    #                 6 - transport protocol
    #                 7 - application protocol
    #                 by all those parameters make the most accurate rating for the best firewall enforcer desicion

    #                 THE PACKET PARAMETERS ARE:

    #                 1 - {packet_event.direction}
    #                 2 - {packet_event.source_ip}
    #                 3 - {packet_event.source_port}
    #                 4 - {packet_event.destination_ip}
    #                 5 - {packet_event.destination_port}
    #                 6 - {packet_event.transport_protocol}
    #                 7 - {packet_event.application_protocol}

    #         """

    #     respone = client.models.generate_content(model="gemini-1.5-flash",contents=request)
    #     response_txt = respone.text

    #     desicion = response_txt.split(",")[0]

    #     print("ai desicion is ->" , desicion)

    #     return desicion

