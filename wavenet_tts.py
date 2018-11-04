#!/usr/bin/python3
# coding: utf8

from google.cloud import texttospeech
import os
from sys import argv
from subprocess import call
import hashlib
import locale
import requests
import pytoml

# have to set google_creds in snips.toml
# https://console.cloud.google.com/apis/credentials/serviceaccountkey

GOOGLE_CREDS = ""

with open("/etc/snips.toml", 'r') as f:
    conf = pytoml.load(f)
    GOOGLE_CREDS = conf["snips-tts"]['google_creds']


# Temp folder where the wav files will be stored
TMP_FOLDER = "/tmp/jarvis/"

# Player program
SOUND_PLAYER = "aplay"

text = str(argv[1]).encode('utf-8')

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_CREDS
lang = locale.getdefaultlocale()[0]

# create the cache dir
if not os.path.isdir(TMP_FOLDER):
    os.mkdir(TMP_FOLDER)

# check if we have a connection
def check_internet():
    try:
        r = requests.get('http://clients3.google.com/generate_204', timeout=2)
        if r.status_code != 204:
            raise requests.ConnectionError
        print("online")
        return True
    except requests.ConnectionError:
        print("offline")
    return False


def translate(t):
    print("Google ?")
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(text=t)
    voice = texttospeech.types.VoiceSelectionParams(
        language_code=lang,
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16)
    response = client.synthesize_speech(synthesis_input, voice, audio_config)
    return response.audio_content


def main():
    # cache filename 
    h = hashlib.sha256(text).hexdigest()

    # Do we already have the file ?
    if not os.path.isfile(TMP_FOLDER + h + '.wav'):
        internet = check_internet()
        if internet:
            resp = translate(text)
            with open(TMP_FOLDER + h + '.wav', 'wb') as out:
                out.write(resp)
        else:
            call(["pico2wave", "-w", TMP_FOLDER + h + ".wav", "-l", lang.replace('_', '-'), text])
        call([SOUND_PLAYER, TMP_FOLDER + h + ".wav"])
        if not internet and os.path.isfile(TMP_FOLDER + h + '.wav'):
            os.remove(TMP_FOLDER + h + '.wav')
    else:
        call([SOUND_PLAYER, TMP_FOLDER + h + ".wav"])


if __name__ == '__main__':
    main()
