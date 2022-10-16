from playsound import playsound
from gtts import gTTS

def speak(response):
    tts = gTTS(response)
    tts.save('response.mp3')
    playsound('./response.mp3')