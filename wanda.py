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


def monitora_audio():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print("Aguardando o Comando: ")
            audio = microfone.listen(source)   
            try:
                trigger = microfone.recognize_google_cloud(audio, credentials_json="wanda-python-assistent-be1eab582aff.json", language="pt-BR")
                trigger = trigger.lower()
                print("Você disse: " + trigger)
                
                if hotword in trigger:
                    print("Comando reconhecido ", trigger)
                    responde(feedback)
                    executa_comandos(trigger)
                    break
                   
            except sr.UnknownValueError:
                print("Google Cloud Speech could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Cloud Speech service; {0}".format(e))
    return trigger
def responde(arquivo):
    call (["afplay", "audios/" + arquivo +".mp3"])
def cria_audio(mensagem):
    # Inicializa o cliente
    client = texttospeech.TextToSpeechClient()
    print('iniciou o client')
    # Configura o texto e a voz
    input_text = texttospeech.SynthesisInput(text=mensagem)  # Correção aqui
    voice = texttospeech.VoiceSelectionParams(
        language_code="pt-BR",
        name="pt-BR-Neural2-C",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )
    print('configurou o texto e voz')

    # Configura o tipo de áudio
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    print('configurou o tipo de audio')

    # Realiza a síntese de fala
    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )
    print('configurou sintese da fala')
    # Salva o áudio
    if not os.path.exists('audios'):
        os.makedirs('audios')
    with open("audios/mensagem.mp3", "wb") as out:
        out.write(response.audio_content)
    print('salvou o audio')
    responde('mensagem')
def executa_comandos(trigger):
    print('Executando Comandos')
    if "notícias" in trigger:
        ultimas_noticias()
        
    elif "toca" in trigger and "nice" in trigger:
        playlists("nice")
    elif "toca" in trigger and "clássica" in trigger:
        playlists("nice")
    elif "tempo agora" in trigger:
        previsao_do_tempo(tempo=True)
    elif "temperatura" in trigger:
        previsao_do_tempo(minmax=True)
                    
    else:
        mensagem = trigger.strip(hotword)
        cria_audio(mensagem)
        print('Comando Invalido', mensagem) 
        responde('comando_invalido')
                   
def ultimas_noticias():
     print('Buscando notícias')
     site = get('https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt')
     noticias = BeautifulSoup(markup=site.text, features='lxml-xml')


     for item in noticias.findAll('item')[:5]:
         mensagem = item.title.text
         cria_audio(mensagem)
         print(mensagem)
def playlists(album):
    if album == 'nice':
        browser.open('https://open.spotify.com/track/18GiV1BaXzPVYpp9rmOg0E?si=2b4919a6741445cb') 
    elif album == 'clássica':
        browser.open('https://open.spotify.com/track/2qhB0MjxHZV95QrORat7xe?si=3df219fa831643e6')

def previsao_do_tempo(tempo=False, minmax=False):
    site = get('https://api.openweathermap.org/data/2.5/weather?id=3448439&APPID=a8ff64034aae9cc740e8268f278f8e41&units=metric&lang=pt')
    clima = site.json()
    # print(json.dumps(clima, indent=4))
    temperatura = math.floor(clima['main']['temp'])  
    minima = math.floor(clima['main']['temp_min'])  
    maxima = math.floor(clima['main']['temp_max'])  
    descricao=clima['weather'][0]['description']
    if tempo:
        mensagem = f"Agora está {temperatura} graus com {descricao}"
    if minmax:
        mensagem = f"Mínima de {minima} e Máxima de {maxima} graus"
    cria_audio(mensagem)
def main():
    while True:
        monitora_audio()
                
main()

  