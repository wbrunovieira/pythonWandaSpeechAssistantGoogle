from gtts import gTTS


tts = gTTS(text='Oi Bruninho, a sua Wanda ta aqui', lang='pt-br')
tts.save('audios/hello_wanda.mp3')