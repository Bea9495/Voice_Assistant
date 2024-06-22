import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pytz
import os
import time
from audio_utils import speak


SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
MONTHS = ["enero", "febrero", "marzo", "abril", "mayo", "junio","julio", "agosto", "septiembre","octubre", "noviembre", "diciembre"]
DAYS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
DAY_EXTENTIONS = ["ro", "to", "mo", "do"]


def authenticate_google():
    """Autentica a Google Calendar API y devuelve el servicio."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # Si no hay credenciales válidas disponibles, permite que el usuario inicie sesión.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Guarda las credenciales para la próxima ejecución
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    service = build("calendar", "v3", credentials=creds)
    return service

#funcion para obtener los eventos del calendario
def get_events(day, service):
    #llamamos al calendario API
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    events_result = service.events().list(
        calendarId="primary",
        timeMin= date.isoformat(),
        timeMax = end_date.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute()
    
    events = events_result.get("items", [])

    if not events:
        speak("No tienes eventos próximos.")
        # speak("No upcoming events found.")
    else:
        speak(f"Tienes {len(events)} eventos ese día.")
        # speak(f"You have {len(events)} events on this day.")

        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])
            start_time = str(start.split("T")[1].split("+")[0])
            if int(start_time.split(":")[0]) < 12:
                start_time = start_time + "am"
            else:
                start_time = str(int(start_time.split(":")[0])-12)
                start_time = start_time + "pm" 

            speak(event["summary"] + " a las " + start_time)

#funcion para obtener la fecha
def get_date(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count("hoy") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass

    # ajustamos el año si el mes es anterior al mes actual
    if month < today.month and month != -1: 
        year = year+1

    # Asignamos el mes actual si no se encuentra un mes
    if month == -1 and day != -1:  
        if day < today.day:
            month = today.month + 1
        else:
            month = today.month

    # calculamos la fecha basada en el dia de la semana
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif += 7
            if text.count("próximo") >= 1:
                dif += 7

        return today + datetime.timedelta(dif)

    if day != -1: 
        return datetime.date(month=month, day=day, year=year)