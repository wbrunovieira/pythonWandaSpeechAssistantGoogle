import speech_recognition as sr
from subprocess import call
from requests import get
from gtts import gTTS
from bs4 import BeautifulSoup
from google.cloud import texttospeech
import webbrowser as browser
import json
import math

feedback = "feedback"
hotword = "gata"

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "wanda-python-assistent-be1eab582aff.json"

def monitor_audio():
    microphone = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print("Aguardando o Comando: ")
            audio = microphone.listen(source)
            try:
                trigger = microphone.recognize_google_cloud(audio, credentials_json="wanda-python-assistent-be1eab582aff.json", language="pt-BR")
                trigger = trigger.lower()
                print("Você disse: " + trigger)

                if hotword in trigger:
                    print("Comando reconhecido ", trigger)
                    respond(feedback)
                    execute_commands(trigger)
                    break

            except sr.UnknownValueError:
                print("Google Cloud Speech could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Cloud Speech service; {0}".format(e))
    return trigger

def respond(audio_file):
    call(["afplay", "audios/" + audio_file + ".mp3"])

def create_audio(message):
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=message)
    voice = texttospeech.VoiceSelectionParams(
        language_code="pt-BR",
        name="pt-BR-Neural2-C",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )
    if not os.path.exists('audios'):
        os.makedirs('audios')
    with open("audios/mensagem.mp3", "wb") as out:
        out.write(response.audio_content)
    respond('mensagem')

def execute_commands(trigger):
    if "notícias" in trigger:
        fetch_latest_news()
    elif "toca" in trigger and "nice" in trigger:
        play_playlist("nice")
    elif "toca" in trigger and "clássica" in trigger:
        play_playlist("clássica")
    elif "tempo agora" in trigger:
        fetch_weather_forecast(tempo=True)
    elif "temperatura" in trigger:
        fetch_weather_forecast(minmax=True)
    else:
        message = trigger.strip(hotword)
        create_audio(message)
        print('Comando Invalido', message)
        respond('comando_invalido')

def fetch_latest_news():
    site = get('https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt')
    news = BeautifulSoup(markup=site.text, features='lxml-xml')
    for item in news.findAll('item')[:5]:
        message = item.title.text
        create_audio(message)

def play_playlist(album):
    if album == 'nice':
        browser.open('https://open.spotify.com/track/18GiV1BaXzPVYpp9rmOg0E?si=2b4919a6741445cb')
    elif album == 'clássica':
        browser.open('https://open.spotify.com/track/2qhB0MjxHZV95QrORat7xe?si=3df219fa831643e6')

def fetch_weather_forecast(tempo=False, minmax=False):
    site = get('https://api.openweathermap.org/data/2.5/weather?id=3448439&APPID=a8ff64034aae9cc740e8268f278f8e41&units=metric&lang=pt')
    weather = site.json()
    temperature = math.floor(weather['main']['temp'])
    minimum = math.floor(weather['main']['temp_min'])
    maximum = math.floor(weather['main']['temp_max'])
    description = weather['weather'][0]['description']
    if tempo:
        message = f"Agora está {temperature} graus com {description}"
    if minmax:
        message = f"Mínima de {minimum} e Máxima de {maximum} graus"
    create_audio(message)

def main():
    while True:
        monitor_audio()

main()
