import datetime
import subprocess


#funcion para tomar notas
def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-nota.txt"
    with open(file_name, "w") as f:
        f.write(text)
    # sublime = "C:\Windows\system32\notepad.exe" en caso de que tuviera otro procesador de texto
    subprocess.Popen(["notepad.exe", file_name])