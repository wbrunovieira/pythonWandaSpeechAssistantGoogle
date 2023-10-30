from gtts import gTTS

from subprocess import call    #OSX e Linux
# from playsound import playsound #windows
def cria_audio(audio):
    tts = gTTS(audio, lang='pt-br')
    tts.save('audios/feedback.mp3')

    call (['afplay', 'audios/hello_wanda.mp3']) # Mac
# call (['aplay', 'audios/hello_wanda.mp3']) # Linux
#  playsound('audios/bem_vindo.mp3') # Windows
cria_audio('Oi meu amor, a sua Wanda ta aqui')