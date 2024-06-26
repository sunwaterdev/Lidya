# Lidya project core.
# For security reasons, please do not modify this part of the code.
# Made by SunWater_

# Imports
import speech_recognition as sr
import time
import json
import libs.tts as tts
import libs.config as config
import libs.llm_con as llm_con
import libs.pluginmanager as pluginmanager

# Load configuration
CONF = config.Config('./config')

# Init STT & TTS
r = sr.Recognizer()
tts = tts.TTS(CONF.get_lang(), CONF.get_tts_model())

# Load plugins:
pm = pluginmanager.PluginManager()

# Init LLM
llm = llm_con.Connector(CONF.get_main_model(), CONF.get_main_service(), CONF.get_apikeys(CONF.get_main_service()), CONF.get_prompt().replace('[PLUGINS_LIST]', str(pm.load_plugins())))
print(llm.prompt)

# Main func
def listen_and_repeat(last_communication):
    with sr.Microphone() as source:
        audio = r.listen(source)
        user_message = r.recognize_google(audio, language=CONF.get_lang())

        if (time.time() - last_communication) < 5:
            present = True
            message = user_message
        else:
            print('[*] New communication detected... ')
            llm.reset()
            present = False
            message = None
            for phrase in CONF.get_wakewords():
                if phrase.lower() in user_message.lower():
                    present = True
                    message = user_message.lower().replace(phrase.lower(), '')
                    break

        if present == True:
            print('[*] Generation process starting... ')
            print(f'[*] API query: {CONF.get_main_service()}, with model {CONF.get_main_model()}...')
            
            llm_result = json.loads(llm.interact(message))

            plugin_result = pm.process_actions(llm_result['actions'])

            if plugin_result != {}:
                llm_result = json.loads(llm.interact('PLUGIN RESULTS:' + str(plugin_result)))

            print('[*] Generating audio... ')
            tts.play_generate_audio(llm_result['message'])

            print('[*] Process finished. ')
            last_communication = time.time()
        
        return last_communication

last_communication = 0
while 1:
    last_communication = listen_and_repeat(last_communication)
