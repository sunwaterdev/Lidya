# Lidya project core.
# For security reasons, please do not modify this part of the code.
# Made by SunWater_

import speech_recognition as sr
from coqui_tts import TTSCoqui

# Mise en place de la reconnaissance vocale
r = sr.Recognizer()
tts = TTSCoqui()

# Fonction pour écouter et répéter
def listen_and_repeat():
    with sr.Microphone() as source:
        # Enregistrement du message vocal
        print("Dites quelque chose après le signal 'OK'")
        audio = r.listen(source)
        print('here')
        print(r.recognize_google(audio, language='fr-FR'))
        try:
            # Reconnaissance vocale du message enregistré
            text = r.recognize_google(audio, language='fr-FR')
            print("Vous avez dit: " + text)
            # Synthèse vocale du texte reconnu
            tts.synthesize(text, "output.wav")
        except sr.UnknownValueError:
            print("Impossible de reconnaître la parole")
        except sr.RequestError:
            print("Problème de connexion à l'API de reconnaissance vocale")

# Appel de la fonction pour écouter et répéter
listen_and_repeat()
