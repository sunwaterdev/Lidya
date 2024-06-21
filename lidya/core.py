# Lidya project core.
# For security reasons, please do not modify this part of the code.
# Made by SunWater_

import speech_recognition as sr
import libs.tts as tts

r = sr.Recognizer()
tts = tts.TTS('fr-FR', 'siwis-medium')

def listen_and_repeat():
    with sr.Microphone() as source:
        audio = r.listen(source)
        user_message = r.recognize_google(audio, language='fr-FR')

        # Check if message contain "ok lidya"
        print(user_message)
        if user_message.split()[0] in ['ok', 'Ok', 'okay', 'Okay'] and user_message.split()[1] in ['Lidya', 'lidya']:
            pass

listen_and_repeat()
