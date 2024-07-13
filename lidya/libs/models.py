"""Lidya model loader v0.0.1. Created by SunWater_"""
import dimits
import requests
from lidya.libs import config

def download_file(url):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

class ModelManager:
    def __init__(self):
        self.config = config.Config('./config')

    def load_active_model(self):
        main_model = self.config.get_main_model()
        model = dimits.TextToSpeechModel(f'./models/{main_model}/{main_model}')
        return model

    def download_model(self, url):
        model = requests.get(url, timeout=1000).text
        self.config.config['main_model'] = download_file(url)
