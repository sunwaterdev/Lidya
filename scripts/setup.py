"""
Setup wizard for the Lidya assistant. 
Version: 0.0.1-alpha - Created by SunWater_
License: GPLv3"""

# Imports
import re
import json
import requests

CONFIG_URL = "https://pastebin.com/raw/Rmu8qxB9"
MESSAGES_URL = "https://pastebin.com/raw/4BaVZZS7"
KEYS_URL = "https://pastebin.com/raw/7uK49WRr"
WAKEWORDS_URL = "https://pastebin.com/raw/1WGYn2Zk"

print('[*] Collecting default configurations... ')
CONFIG = json.loads(requests.get(CONFIG_URL, timeout=500).text)
MESSAGES = json.loads(requests.get(MESSAGES_URL, timeout=500).text)
KEYS = json.loads(requests.get(KEYS_URL, timeout=500).text)
WAKEWORDS = json.loads(requests.get(WAKEWORDS_URL, timeout=500).text)

print('[*] Setup wizard is ready! Please complete few questions bellow.')

# Collect OpenAI key
VALIDATED = False
while VALIDATED is False:
    OPENAI_KEY = input('[?] We need a working API key for OpenAI: ')

    # Validating key
    api_key_pattern = re.compile(r"sk-*")
    if bool(api_key_pattern.match(OPENAI_KEY)):
        VALIDATED = True
    else:
        VALIDATED = False
        print('[!] The key does not appear to be valid. Check if there is a line break at the end.')

print('[*] Updating configuration... ')
KEYS['openai'] = OPENAI_KEY



# Collect favorite model
OPENAI_FAV_MODEL = input('[?] What is your favorite OpenAI llm model [gpt-3.5-turbo]: ')

if OPENAI_FAV_MODEL == "":
    print('[*] Nothing provied. Choosing gpt-3.5-turbo')
    OPENAI_FAV_MODEL = "gpt-3.5-turbo"

print('[*] Updating configuration... ')
CONFIG['main_model'] = OPENAI_FAV_MODEL
