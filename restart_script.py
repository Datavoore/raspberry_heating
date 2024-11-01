import subprocess
import psutil

found_serv, found_main = False, False

for process in psutil.process_iter():
    if "server:app" in process.cmdline():
        found_serv = True
    if "/home/pi/Documents/raspberry_heating/main.py" in process.cmdline():
        found_main = True

if not found_serv:
    print("Server not running, starting it")
    subprocess.Popen(
        [
            "nohup",
            "uvicorn",
            "--app-dir",
            "/home/pi/Documents/raspberry_heating",
            "server:app",
            "--reload",
            "--host",
            "0.0.0.0",
            "--port",
            "8042",
        ]
    )
if not found_main:
    print("Main not running, starting it")
    subprocess.Popen(
        ["nohup", "python3", "/home/pi/Documents/raspberry_heating/main.py"]
    )
