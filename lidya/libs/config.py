# Lidya config loader
# Imports
import json

# Config class


class Config:
    def __init__(self, config_folder):
        wakewords_file = config_folder + "/wakewords.json"
        config_file = config_folder + "/config.json"
        keys_file = config_folder + "/keys.json"
        messages_file = config_folder + "/messages.json"

        self.config_folder = config_folder

        with json.load(open(wakewords_file, "r")) as f:
            self.wakewords = f

        with json.load(open(config_file, "r")) as f:
            self.config = f

        with json.load(open(keys_file, "r")) as f:
            self.keys = f

        with json.load(open(messages_file, "r")) as f:
            self.messages = f

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
