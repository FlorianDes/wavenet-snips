#!/usr/bin/python3
# coding: utf8

from google.cloud import texttospeech_v1beta1 as texttospeech
import os
from sys import argv, exit
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

if len(argv) > 2:
    output = str(argv[1])

    text = str(argv[2]).encode('utf-8')
else:
    exit()

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_CREDS
LANG = locale.getdefaultlocale()[0]

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
        language_code=LANG,
        name="fr-FR-Wavenet-A")
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16,
        effects_profile_id=["medium-bluetooth-speaker-class-device"],
        pitch=-2.00)
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
            with open(output, 'wb') as out:
                out.write(resp)
        else:
            call(["pico2wave", "-w", output, "-l", LANG.replace('_', '-'), text])
    else:
        os.popen('cp %s%s.wav %s' % (TMP_FOLDER, h, output))

if __name__ == '__main__':
    main()
