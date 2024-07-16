"""
Main Lidya launcher
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
import vosk
import pyaudio
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

# Init STT
print('[*] Loading STT... ')
model = vosk.Model(f"./models/{CONF.config['stt_model']}/{CONF.config['stt_model']}")
rec = vosk.KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8192)

# Init TTS
print('[*] Loading TTS... ')
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
    CONF.get_prompt().replace("[PLUGINS_LIST]", str(pm.load_plugins())),
)

# Main func
print('[*] Starting... ')
def listen_and_repeat(last_communication):
    """Main listen & repeat function"""
    user_message = None
    data = stream.read(4096)
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        user_message = result['text']

    if user_message:
        #user_message = "ok lydia execute la commande 'weather' pour récupérer la météo."
        if (time.time() - last_communication) < 10:
            communication = True
            message = user_message
        else:
            print("[*] New communication detected... ")
            llm.reset()
            communication = False
            message = None
            for phrase in CONF.get_wakewords():
                if phrase.lower() in user_message.lower():
                    communication = True
                    message = user_message.lower().replace(phrase.lower(), "")
                    break

        if communication:
            song = AudioSegment.from_file("./lidya/ressources/sounds/success_blip.mp3",
                                        format="mp3")
            play(song)
            print("[*] Generation process starting... ")
            print(
                f"[*] API query: {CONF.get_main_service()}, with model {CONF.get_main_model()}..."
            )
            try:
                llm_result = json.loads(llm.interact(message))
            except openai.APIConnectionError:
                song = AudioSegment.from_file("./lidya/ressources/sounds/fail_blip.mp3",
                                            format="mp3")
                play(song)
                tts.play_generate_audio(
                    CONF.get_messages()[CONF.get_lang()]["llm_error"]
                )
                print(
                    "[x] Please check LLM configuration. Cannot connect the services "
                )
                sys.exit(21)
            print('[*] Processing plugins... ')
            if isinstance(llm_result, dict) and "actions" in llm_result.keys():
                plugin_result = pm.process_actions(llm_result["actions"])
            else:
                plugin_result = None
                print('[x] The LLM forgot to provide any actions. Skiped.')
            if plugin_result:
                print('[!] Plugin usage detected... ')
                llm_result = json.loads(
                    llm.interact("PLUGIN RESULTS:" + str(plugin_result))
                )
            print("[*] Generating audio... ")
            if isinstance(llm_result, dict):
                if "message" in llm_result.keys():
                    tts.play_generate_audio(llm_result["message"])
                if "finished" in llm_result.keys():
                    if llm_result["finished"] == True:
                        last_communication = 0
                    else:
                        last_communication = time.time()
                else:
                    last_communication = time.time()
            else:
                last_communication = time.time()
                song = AudioSegment.from_file("./lidya/ressources/sounds/fail_blip.mp3",
                                            format="mp3")
                play(song)
                tts.play_generate_audio(llm_result)
            print("[*] Process finished. ")

        return last_communication
    else:
        return last_communication

# Stop event
LAST_COMMUNICATION = 0
while 1:
    time.sleep(0.1)
    try:
        LAST_COMMUNICATION = listen_and_repeat(LAST_COMMUNICATION)
    except sr.exceptions.UnknownValueError:
        pass
