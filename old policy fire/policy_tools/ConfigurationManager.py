import json

class ConfigurationManager:
    def load_disallowlist(self, path):
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
