"""Lidya config loader."""
# Lidya config loader
# Imports
import json

# Config class


class Config:
    """Config loader"""
    def __init__(self, config_folder):
        wakewords_file = config_folder + "/wakewords.json"
        config_file = config_folder + "/config.json"
        keys_file = config_folder + "/keys.json"
        messages_file = config_folder + "/messages.json"

        self.config_folder = config_folder

        with json.load(open(wakewords_file, "r", encoding="utf-8")) as f:
            self.wakewords = f

        with json.load(open(config_file, "r", encoding="utf-8")) as f:
            self.config = f

        with json.load(open(keys_file, "r", encoding="utf-8")) as f:
            self.keys = f

        with json.load(open(messages_file, "r", encoding="utf-8")) as f:
            self.messages = f

        self.lang = self.config["main_language"]

    def get_wakewords(self):
        """Lidya wakewords loeader"""
        return self.wakewords[self.lang]

    def get_lang(self):
        """Lidya language loader"""
        return self.lang

    def get_tts_model(self):
        """Lidya TTS model/voice loader"""
        return self.config["tts_model"]

    def get_apikeys(self, service):
        """Lidya services keys loader"""
        return self.keys[service]

    def get_main_service(self):
        """Lidya LLM services loader"""
        return self.config["main_service"]

    def get_main_model(self):
        """Lidya LLM models loader"""
        return self.config["main_model"]

    def get_prompt(self):
        """Lidya LLM prompt loader"""
        return self.config["prompt"]

    def get_messages(self):
        """Lidya pre-created messages loader"""
        return self.messages
