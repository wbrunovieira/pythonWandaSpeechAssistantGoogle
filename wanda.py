import speech_recognition as sr



import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "wanda-python-assistent-be1eab582aff.json"


def monitora_audio():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        print("Aguardando o Comando: ")
        audio = microfone.listen(source)
        
            # recognize speech using Google Cloud Speech
   
    try:
       print("Google Cloud Speech thinks you said " + microfone.recognize_google_cloud(audio, credentials_json="wanda-python-assistent-be1eab582aff.json", language="pt-BR"))

    except sr.UnknownValueError:
        print("Google Cloud Speech could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Cloud Speech service; {0}".format(e))
monitora_audio()
   