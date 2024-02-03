from fastapi import FastAPI
from GPIO import *
from sonde import Sonde
from config import sondes_paths, favicon_path
from fastapi.responses import FileResponse

sondes = {}
for i in range(len(sondes_paths)):
    try :
        sondes[i + 1] = Sonde(sondes_paths[i])
    except FileNotFoundError:
        pass

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Papa"}


@app.get("/temperature/{sonde_number}")
async def get_temp(sonde_number: int):
    sonde = sondes.get(sonde_number)
    if sonde:
        temperature = sonde.get_temperature()
        return {f"Temperature Sonde {sonde_number}": temperature}
    else:
        return {f"Sonde not found"}


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)
