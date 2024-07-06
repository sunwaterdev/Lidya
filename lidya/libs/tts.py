# Imports
from dimits import Dimits

# Main class


class TTS:
    def __init__(self, lang, voice):
        self.lang = lang
        self.voice = voice
        self.model = lang + "-" + voice

        self.dt = Dimits(self.model)

    def generate_audio(self, text, location):
        self.dt.text_2_audio_file(
            text, location.split("/")[-1], "/".join(location.split("/")[0:-1])
        )
        return location

    def play_generate_audio(self, text):
        self.dt.text_2_speech(text)


# Tests
if __name__ == "__main__":
    tts = TTS("fr_FR", "siwis-medium")
    tts.generate_audio("salut les amis", "./test.wav")
    tts.play_generate_audio("Salut les amis")
