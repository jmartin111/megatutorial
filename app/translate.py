#! .venv/bin/python

import requests
import json
import os

from flask_babel import _
from dotenv import load_dotenv
from google.cloud import translate_v2 as translate

from app import blog

load_dotenv()

class Translate():
    def __init__(self, phrase, target_lang, source_lang=None):
        self.phrase = phrase
        self.source_lang = source_lang
        self.target_lang = target_lang


    def client_translate(self) -> dict:
        """Translates text into the target language.

        Target must be an ISO 639-1 language code.
        See https://g.co/cloud/translate/v2/translate-reference#supported_languages
        """
        # service acct creds stored in environment
        translate_client = translate.Client()

        if isinstance(self.phrase, bytes):
            self.phrase = self.phrase.decode("utf-8")

        print(self.phrase, type(self.phrase))

        # Text can also be a sequence of strings, in which case this method
        # will return a sequence of results for each text.
        result = translate_client.translate(self.phrase, target_language=self.target_lang)

        print("Text: {}".format(result["input"]))
        print("Translation: {}".format(result["translatedText"]))
        print("Detected source language: {}".format(result["detectedSourceLanguage"]))

        return result
    
    def http_translate(self):
        key = blog.config['G_API_KEY']
        # key = os.environ.get('G_API_KEY')

        if not key: 
            return _('Failed to authenticate witht the translation service')
        
        url = f"https://translation.googleapis.com/language/translate/v2?key={key}"

        my_data = {
        "q": [self.phrase],
        "source_lang": self.source_lang,
        "target_lang": self.target_lang
        }

        payload = json.dumps(my_data)

        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, data=payload)

        if response.status_code != 200:
            return _('The translation service failed')

        return response.json()['data']['translations'][0]['translatedText']
