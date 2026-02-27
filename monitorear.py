import time
import subprocess
from threading import Timer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

file_to_watch = "mediciones/data.txt"
script_to_run = "mediciones_largas.py"
counter_file = "contador.txt"

# Config
debounce_seconds = 0.5  # espera 500ms después del último cambio
timer = None
running = False

with open(counter_file, "w") as f:
    f.write("0\n")

def ejecutar_script():
    global running
    running = True
    #print(f"Ejecutando {script_to_run}...")

    try:
        with open(counter_file, "r") as f:
            num = int(f.read().strip())

        subprocess.run(["python3", script_to_run, str(num)])
        with open(counter_file, "w") as f:
            f.write(str(num + 1))
    finally:
        running = False

class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        global timer, running

        if os.path.abspath(event.src_path) != os.path.abspath(file_to_watch):
            return

        if running:
            print("Script aún corriendo, evento ignorado.")
            return

        # Cancela el timer previo (si lo hay) y reinicia uno nuevo
        if timer is not None:
            timer.cancel()

        #print("Evento detectado. Esperando estabilización...")
        timer = Timer(debounce_seconds, ejecutar_script)
        timer.start()

observer = Observer()
observer.schedule(FileChangeHandler(), path="mediciones", recursive=False)
observer.start()

print(f"Esperando cambios en {file_to_watch}...")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()

