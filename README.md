# wavenet-snips
TTS for snips using Google Wavenet
### Requirement
- pip3 install google-cloud-texttospeech requests
- Get the service account key file here https://console.cloud.google.com/apis/credentials/serviceaccountkey
- Change the line GOOGLE_CREDS = "CHANGE ME" with the path of the credentials json previously downloaded

### In snips.toml
customtts = { command = ["[PATH to the file]", "%%TEXT%%"] }
