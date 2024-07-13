"""
Main continuous Lidya launcher
Created by SunWater_
"""

# Lidya project core.
# For security reasons, please do not modify this part of the code.
# Made by SunWater_

# Imports
import time
import json
import sys
import openai
import requests
from libs import tts
from libs import config
from libs import llm_con
from libs import pluginmanager
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr

# Version var
__VERSION__ = "0.0.1"
LAST_VERSION_URL = "https://pastebin.com/raw/VVp9rRhb"

last_version = requests.get(LAST_VERSION_URL, timeout=100).text

# Edit path
sys.path.append("./")

# Load configuration
print('[*] Loading config... ')
CONF = config.Config("./config")

# Init STT & TTS
print('[*] Loading STT & TTS... ')
r = sr.Recognizer()
tts = tts.TTS(CONF.get_tts_model())

# Check version
if last_version != __VERSION__:
    tts.play_generate_audio(CONF.get_messages()[CONF.get_lang()]['version_deprec'])

# Load plugins:
print('[*] Loading plugins... ')
pm = pluginmanager.PluginManager()
pm.load_plugins()

# Init LLM
print('[*] Loading LLM... ')
llm = llm_con.Connector(
    CONF.get_main_model(),
    CONF.get_main_service(),
    CONF.get_apikeys(CONF.get_main_service()),
    CONF.get_prompt().replace("[PLUGINS_LIST]", str(pm.load_plugins()))+CONF.config['continous_prompt'],
)

def main():
    with sr.Microphone() as source:
        audio = r.listen(source)
        user_message = r.recognize_google(audio, language=CONF.get_lang())

        llm_result = json.loads(llm.interact(user_message))
        
        llm_tosay = None

        if not llm_result == {}:
            if isinstance(llm_result, dict):
                if "actions" in llm_result.keys():
                    plugin_result = pm.process_actions(llm_result["actions"])
                    if plugin_result:
                        print('[!] Plugin usage detected... ')
                        llm_result = json.loads(
                            llm.interact("PLUGIN RESULTS:" + str(plugin_result))
                        )
                if "message" in llm_result.keys():
                    llm_tosay = llm_result['message']

            else:
                llm_tosay = llm_result

        if llm_tosay:
            tts.play_generate_audio(llm_tosay)

while 1:
    try:
        main()
    except:
        pass