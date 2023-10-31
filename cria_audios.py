from gtts import gTTS

from subprocess import call    #OSX e Linux
# from playsound import playsound #windows
def cria_audio(audio):
    tts = gTTS(audio, lang='pt-br')
    tts.save('audios/comando_invalido.mp3')

    call (['afplay', 'audios/comando_invalido.mp3']) # Mac
# call (['aplay', 'audios/hello_wanda.mp3']) # Linux
#  playsound('audios/bem_vindo.mp3') # Windows
cria_audio('desculpe amor, não sou paga para isso')