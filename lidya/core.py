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
from libs import tts
from libs import config
from libs import llm_con
from libs import pluginmanager
import speech_recognition as sr
from playsound import playsound

# Edit path
sys.path.append("./")

# Load configuration
CONF = config.Config("./config")

# Init STT & TTS
r = sr.Recognizer()
tts = tts.TTS(CONF.get_lang(), CONF.get_tts_model())

# Load plugins:
pm = pluginmanager.PluginManager()

# Init LLM
llm = llm_con.Connector(
    CONF.get_main_model(),
    CONF.get_main_service(),
    CONF.get_apikeys(CONF.get_main_service()),
    CONF.get_prompt().replace("[PLUGINS_LIST]", str(pm.load_plugins())),
)

# Stop event
stop = False

# Main func


def listen_and_repeat(last_communication):
    with sr.Microphone() as source:
        audio = r.listen(source)
        user_message = r.recognize_google(audio, language=CONF.get_lang())

        # user_message = "ok lydia quel heure est il?"

        if (time.time() - last_communication) < 5:
            present = True
            message = user_message
        else:
            print("[*] New communication detected... ")
            llm.reset()
            present = False
            message = None
            for phrase in CONF.get_wakewords():
                if phrase.lower() in user_message.lower():
                    present = True
                    message = user_message.lower().replace(phrase.lower(), "")
                    break

        if present:
            playsound("./lidya/ressources/sounds/success_blip.mp3")
            print("[*] Generation process starting... ")
            print(
                f"[*] API query: {CONF.get_main_service()}, with model {CONF.get_main_model()}..."
            )

            try:
                llm_result = json.loads(llm.interact(message))
            except BaseException:
                playsound("./lidya/ressources/sounds/fail_blip.mp3")
                tts.play_generate_audio(
                    CONF.get_messages()[CONF.get_lang()]["llm_error"]
                )
                print(
                    "[x] Please check LLM configuration. Cannot connect the services "
                )
                stop = (True, 21)

            plugin_result = pm.process_actions(llm_result["actions"])

            if not plugin_result:
                llm_result = json.loads(
                    llm.interact("PLUGIN RESULTS:" + str(plugin_result))
                )

            print("[*] Generating audio... ")
            tts.play_generate_audio(llm_result["message"])

            print("[*] Process finished. ")
            last_communication = time.time()

        return last_communication

        time.sleep(10)


last_communication = 0

while stop is False:
    last_communication = listen_and_repeat(last_communication)
