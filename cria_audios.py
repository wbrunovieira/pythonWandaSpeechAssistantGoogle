
from google.cloud import texttospeech
from subprocess import call    #OSX e Linux
# # from playsound import playsound #windows
# def cria_audio(audio):
#     tts = gTTS(audio, lang='pt-br')
#     tts.save('audios/comando_invalido.mp3')

#     call (['afplay', 'audios/comando_invalido.mp3']) # Mac
# # call (['aplay', 'audios/hello_wanda.mp3']) # Linux
# #  playsound('audios/bem_vindo.mp3') # Windows


import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "wanda-python-assistent-be1eab582aff.json"
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
    with open("audios/comando_invalido.mp3", "wb") as out:
        out.write(response.audio_content)
    print('salvou o audio')
    
cria_audio("Bruninho, não sou paga para isso!!!")
call (["afplay", "audios/" + "feedback.mp3"])