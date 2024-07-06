# Lidya config loader
# Imports
import json

# Config class


class Config:
    def __init__(self, config_folder):
        self.wakewords_file = config_folder + "/wakewords.json"
        self.config_file = config_folder + "/config.json"
        self.keys_file = config_folder + "/keys.json"
        self.messages_file = config_folder + "/messages.json"

        self.config_folder = config_folder

        self.wakewords = json.load(open(self.wakewords_file, "r"))
        self.config = json.load(open(self.config_file, "r"))
        self.keys = json.load(open(self.keys_file, "r"))
        self.messages = json.load(open(self.messages_file, "r"))

        self.lang = self.config["main_language"]

    def get_wakewords(self):
        return self.wakewords[self.lang]

    def get_lang(self):
        return self.lang

    def get_tts_model(self):
        return self.config["tts_model"]

    def get_apikeys(self, service):
        return self.keys[service]

    def get_main_service(self):
        return self.config["main_service"]

    def get_main_model(self):
        return self.config["main_model"]

    def get_prompt(self):
        return self.config["prompt"]

    def get_messages(self):
        return self.messages
