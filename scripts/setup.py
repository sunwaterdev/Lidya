"""
Setup wizard for the Lidya assistant. 
Version: 0.0.1-alpha - Created by SunWater_
License: GPLv3"""

# Imports
import re
import sys
import os
import tarfile
import zipfile
import json
import requests
from rich import print as dprint
from rich.console import Console
from rich.prompt import Prompt, Confirm

def strip_extension(fn: str, extensions):
    """Remove extensions from file"""
    for ext in extensions:
        if fn.endswith(ext):
            return fn[: -len(ext)]
    raise ValueError(f"Unexpected extension for filename: {fn}")

console = Console()

CONFIG_URL = "https://pastebin.com/raw/Rmu8qxB9"
MESSAGES_URL = "https://pastebin.com/raw/4BaVZZS7"
KEYS_URL = "https://pastebin.com/raw/7uK49WRr"
WAKEWORDS_URL = "https://pastebin.com/raw/1WGYn2Zk"
TTS_MODEL_URL = "https://pastebin.com/raw/HxxQrcd9"
STT_MODEL_URL = "https://pastebin.com/raw/NNjDjPWE"
CONFIG_FILE = "./config/config.json"
MESSAGES_FILE = "./config/messages.json"
KEYS_FILE = "./config/keys.json"
WAKEWORDS_FILE = "./config/wakewords.json"

try:
    os.mkdir('cache')
    os.mkdir('config')
    os.mkdir('models')
except FileExistsError:
    if not Confirm.ask('[bold yellow][?][/bold yellow] 🤔 It looks like you\'ve \
already set up Lidya. Starting the configuration again will reset Lidya. Do you want to continue?'):
        dprint('[bold blue][*][/bold blue] ✅ The installation was successfully terminated.')
        sys.exit(11)
dprint('[bold blue][*][/bold blue] 💪 The wizard has prepared properly!')

# Collect configuration
with console.status(" 🌐 Fetching configuration... ",
                    spinner="dots12",
                    spinner_style="blue") as progress:
    CONFIG = json.loads(requests.get(CONFIG_URL, timeout=100).text)
    MESSAGES = json.loads(requests.get(MESSAGES_URL, timeout=100).text)
    KEYS = json.loads(requests.get(KEYS_URL, timeout=100).text)
    WAKEWORDS = json.loads(requests.get(WAKEWORDS_URL, timeout=100).text)
    TTS_MODELS = json.loads(requests.get(TTS_MODEL_URL, timeout=100).text)
    STT_MODELS = json.loads(requests.get(STT_MODEL_URL, timeout=100).text)

dprint('[bold blue][*][/bold blue] 🌐 Online default configuration is ready! ')
dprint('[bold blue][*][/bold blue] ⌛ Setup wizard is ready! Please complete few questions bellow.')

# Collect OpenAI key
VALIDATED = False
while VALIDATED is False:
    OPENAI_KEY = Prompt.ask('[bold blue][?][/bold blue] 🔑 We need a working API key for OpenAI')

    # Validating key
    api_key_pattern = re.compile(r"sk-*")
    if bool(api_key_pattern.match(OPENAI_KEY)):
        VALIDATED = True
    else:
        VALIDATED = False
        dprint('[bold yellow][!][/bold yellow] The key does not appear to be valid. '
               + 'Check if there is a line break at the end.')

dprint('[bold blue][*][/bold blue] 📝 Updating configuration... ')
KEYS['openai'] = OPENAI_KEY

# Collect favorite model
OPENAI_FAV_MODEL = Prompt.ask('[bold blue][?][/bold blue] 🤖 What is your favorite OpenAI llm model',
                              default="gpt-3.5-turbo")

dprint('[bold blue][*][/bold blue] 📝 Updating configuration... ')
CONFIG['main_model'] = OPENAI_FAV_MODEL

# Download model
AVILABLES_LANGUAGES = TTS_MODELS.keys()
USER_LANGUAGE = Prompt.ask('[bold blue][?][/bold blue] 🗣️  What language do you speak best',
                           choices=AVILABLES_LANGUAGES, default="en_US")
TTS_MODEL_URL = TTS_MODELS[USER_LANGUAGE]
with console.status(" 🤖 Fetching your TTS model... You have time to get some fresh air! (1/2)",
                    spinner="dots12",
                    spinner_style="blue") as progress:
    local_filename = TTS_MODEL_URL.split('/')[-1]
    with requests.get(TTS_MODEL_URL, stream=True, timeout=1000) as r:
        r.raise_for_status()
        with open("./models/"+local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    with tarfile.open('./models/'+local_filename) as f:
        f.extractall('./models/'+strip_extension(local_filename,
                                                 extensions=[".tar.bz2", ".tar.gz"]))
        f.close()

    CONFIG['tts_model'] = strip_extension(local_filename, extensions=[".tar.bz2", ".tar.gz"])

STT_MODEL = STT_MODELS[USER_LANGUAGE]
with console.status(" 🤖 Fetching your STT model... You have time to get some fresh air! (2/2)",
                    spinner="dots12",
                    spinner_style="blue") as progress:
    local_filename = STT_MODEL.split('/')[-1]
    with requests.get(STT_MODEL, stream=True, timeout=1000) as r:
        r.raise_for_status()
        with open("./models/"+local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    with zipfile.ZipFile("./models/"+local_filename, 'r') as zip_ref:
        zip_ref.extractall("./models/"+strip_extension(local_filename,
                                                       extensions=[".tar.bz2", ".tar.gz", ".zip"]))

    CONFIG['stt_model'] = strip_extension(local_filename,
                                          extensions=[".tar.bz2", ".tar.gz", ".zip"])

CONFIG['main_language'] = USER_LANGUAGE

# Write configuration
dprint('[bold blue][*][/bold blue] 📝 Writing configuration... ')
with open(CONFIG_FILE, 'w', encoding="utf8") as f:
    f.write(json.dumps(CONFIG))

with open(KEYS_FILE, 'w', encoding="utf8") as f:
    f.write(json.dumps(KEYS))

with open(WAKEWORDS_FILE, 'w', encoding="utf8") as f:
    f.write(json.dumps(WAKEWORDS))

with open(MESSAGES_FILE, 'w', encoding="utf8") as f:
    f.write(json.dumps(MESSAGES))

dprint('🎉 The assistant is ready for use! \
Note that you can change the STT \
language and model in the setting\
s outside of the wizard. However, \
we will soon add this functionality to the assistant.')
