from datetime import datetime

class Logger:
    def __init__(self, log_file="firewall.log"):
        self.log_file = log_file

    def log(self, level, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_message = f"{timestamp} [{level}] {message}"

        with open(self.log_file, "a", encoding="utf-8") as file:
            file.write(full_message + "\n")

    def info(self, message):
        self.log("INFO", message)

    def warning(self, message):
        self.log("WARNING", message)

    def error(self, message):
        self.log("ERROR", message)
