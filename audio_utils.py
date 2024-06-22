import pyttsx3
import speech_recognition as sr

# funcion para convertir texto a audio
def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[3].id)
    engine.say(text) 
    engine.runAndWait() 

# Esta funcion detecta la voz de un usuario, traduce el audio a texto y nos lo devuelve 
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("escuchando...")
        audio = r.listen(source)
        said = ""
        try:
            # said = r.recognize_google(audio, language="ES")
            said = r.recognize_whisper(audio_data=audio, language="es", model="base")
            print("dijiste: " + said)
        except Exception as e:
             print("Excepcion: " + str(e))

    return said.lower()   