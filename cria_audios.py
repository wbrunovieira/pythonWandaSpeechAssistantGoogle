# from gtts import gTTS

# from subprocess import call    #OSX e Linux
# # from playsound import playsound #windows
# def cria_audio(audio):
#     tts = gTTS(audio, lang='pt-br')
#     tts.save('audios/comando_invalido.mp3')

#     call (['afplay', 'audios/comando_invalido.mp3']) # Mac
# # call (['aplay', 'audios/hello_wanda.mp3']) # Linux
# #  playsound('audios/bem_vindo.mp3') # Windows
cria_audio('desculpe amor, não sou paga para isso')

from google.cloud import texttospeech

# Inicializa o cliente
client = texttospeech.TextToSpeechClient()

# Configura o texto e a voz
input_text = texttospeech.SynthesisInput(text="Olá, como você está?")
voice = texttospeech.VoiceSelectionParams(
    language_code="pt-BR",
    name="pt-BR-Wavenet-A",
    ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
)

# Configura o tipo de áudio
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# Realiza a síntese de fala
response = client.synthesize_speech(
    input=input_text, voice=voice, audio_config=audio_config
)

# Salva o áudio
with open("output.mp3", "wb") as out:
    out.write(response.audio_content)