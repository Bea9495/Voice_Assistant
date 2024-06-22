# 1 . reproducir sonido
# 2. Obtener entrada microfono
# 3. Vamos a sincronizar el calendario
# 4. preguntar al calendario si tenemos algo
# 5. abrir otras aplicaciones y tomar notas

from audio_utils import speak, get_audio
from calendar_utils import  authenticate_google,get_events, get_date
from note_utils import note

#wakeup word
WAKE = "hola"

SERVICE = authenticate_google()

def handle_calendar(text):
    CALENDAR_STRS = ["qué planes tengo", "qué tengo", "tengo algo"]
    for phrase in CALENDAR_STRS:
        if phrase in text:
            date = get_date(text)
            if date:
                print("Fecha obtenida: ", date)
                get_events(date, SERVICE)
            else:
                speak("No entiendo")

def handle_notes(text):
    NOTE_STRS = ["toma nota", "escribe esto", "haz una nota"]
    for phrase in NOTE_STRS:
        if phrase in text:
                speak("¿Qué quieres que escriba?")
                note_text = get_audio()
                print("nota reconocida: ", note_text)
                note(note_text)
                speak("He tomado nota de eso.")

if __name__== "__main__":
    while True:
        print("Escuchando...")
        text = get_audio()

        if text.count(WAKE) > 0:
            speak("Estoy lista")
            text = get_audio()

            print("Reconocido: ", text)

            handle_calendar(text)
            handle_notes(text)

       
               

    
 