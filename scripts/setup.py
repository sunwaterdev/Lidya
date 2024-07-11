"""
Setup wizard for the Lidya assistant. 
Version: 0.0.1-alpha - Created by SunWater_
License: GPLv3"""

# Imports
import re
import json
import requests
from rich import print as dprint
from rich.console import Console
from rich.prompt import Prompt

console = Console()

CONFIG_URL = "https://pastebin.com/raw/Rmu8qxB9"
MESSAGES_URL = "https://pastebin.com/raw/4BaVZZS7"
KEYS_URL = "https://pastebin.com/raw/7uK49WRr"
WAKEWORDS_URL = "https://pastebin.com/raw/1WGYn2Zk"
CONFIG_FILE = "./config/config.json"
MESSAGES_FILE = "./config/messages.json"
KEYS_FILE = "./config/keys.json"
WAKEWORDS_FILE = "./config/wakewords.json"

dprint('[bold blue][*][/bold blue] Collecting default configurations... ')
with console.status("Fetching configuration... ",
                    spinner="dots10",
                    spinner_style="blue")  as progress:
    CONFIG = json.loads(requests.get(CONFIG_URL, timeout=100).text)
    MESSAGES = json.loads(requests.get(MESSAGES_URL, timeout=100).text)
    KEYS = json.loads(requests.get(KEYS_URL, timeout=100).text)
    WAKEWORDS = json.loads(requests.get(WAKEWORDS_URL, timeout=100).text)
dprint('[bold blue][*][/bold blue] Online default configuration is ready! ')
dprint('[bold blue][*][/bold blue] Setup wizard is ready! Please complete few questions bellow.')

# Collect OpenAI key
VALIDATED = False
while VALIDATED is False:
    OPENAI_KEY = Prompt.ask('[bold blue][?][/bold blue] We need a working API key for OpenAI')

    # Validating key
    api_key_pattern = re.compile(r"sk-*")
    if bool(api_key_pattern.match(OPENAI_KEY)):
        VALIDATED = True
    else:
        VALIDATED = False
        dprint('[bold yellow][!][/bold yellow] The key does not appear to be valid. '
               + 'Check if there is a line break at the end.')

dprint('[bold blue][*][/bold blue] Updating configuration... ')
KEYS['openai'] = OPENAI_KEY

# Collect favorite model
OPENAI_FAV_MODEL = Prompt.ask('[bold blue][?][/bold blue] What is your favorite OpenAI llm model',
                              default="gpt-3.5-turbo")

if OPENAI_FAV_MODEL == "":
    dprint('[bold blue][*][/bold blue] Nothing provied. Choosing gpt-3.5-turbo')
    OPENAI_FAV_MODEL = "gpt-3.5-turbo"

dprint('[bold blue][*][/bold blue] Updating configuration... ')
CONFIG['main_model'] = OPENAI_FAV_MODEL

dprint('[bold blue][*][/bold blue] Writing configuration... ')

with open(CONFIG_FILE, 'w', encoding="utf8") as f:
    f.write(json.dumps(CONFIG))

with open(KEYS_FILE, 'w', encoding="utf8") as f:
    f.write(json.dumps(KEYS))

with open(WAKEWORDS_FILE, 'w', encoding="utf8") as f:
    f.write(json.dumps(WAKEWORDS))

with open(MESSAGES_FILE, 'w', encoding="utf8") as f:
    f.write(json.dumps(MESSAGES))

dprint('The assistant is ready for use! \
Note that you can change the STT \
language and model in the setting\
s outside of the wizard. However, \
we will soon add this functionality to the assistant.')
