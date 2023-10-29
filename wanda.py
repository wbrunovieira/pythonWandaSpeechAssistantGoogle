import speech_recognition as sr

def monitora_microfone():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        print("Aguardando o Comando: ")
        audio = microfone.listen(source)
    try:
        print(microfone.recognize_google(audio,  language='pt-BR'))
                    
    except sr.UnknownValueError:
                    print("Google not understand audio")
    except sr.RequestError as e:
                    print("Could not request results from Google Cloud Speech service;".format(e))

monitora_microfone()








