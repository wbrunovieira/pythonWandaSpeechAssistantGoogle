import speech_recognition as sr
from subprocess import call
from requests import get
from gtts import gTTS
from bs4 import BeautifulSoup
from google.cloud import texttospeech


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
     
def main():
    while True:
        monitora_audio()
                
main()
  