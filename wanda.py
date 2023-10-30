import speech_recognition as sr
from subprocess import call
from requests import requests
from bs4 import BeautifulSoup
hotword = "ata"

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
                    responde('feedback')
                    executa_comandos(trigger)
                    break
            except sr.UnknownValueError:
                print("Google Cloud Speech could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Cloud Speech service; {0}".format(e))
    return trigger
def responde(arquivo):
    call (["afplay", "audios/" + arquivo +".mp3"])

def executa_comandos():
    if "noticias" in trigger:
        ultimas_noticias()   
        
def ultimas_noticias():
     site = requests.get('https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt')
     noticias = BeautifulSoup(site.text, 'html.parser')
     for item in noticias.findAll('item')[:5]:
         mensagem = item.title.text
         print(item.title.text)
     print(noticias.prettify())
def main():
    monitora_audio()
                
main()
   