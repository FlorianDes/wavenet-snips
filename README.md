# wavenet-snips
TTS for snips using Google Wavenet with a fallback to pico2wave if there is no connection
### Requirement
- pip3 install google-cloud-texttospeech requests pytoml
- Get the service account key file here https://console.cloud.google.com/apis/credentials/serviceaccountkey

### In snips.toml
[snips-tts]
customtts = { command = ["[PATH to wavenet_tts.py]", "%%TEXT%%"] }
google_creds = "Path to the json creds file"
