from fastapi import FastAPI
from GPIO import *
from sonde import Sonde
from config import sondes_paths
from fastapi.responses import FileResponse

sondes = {}
for i in range(len(sondes_paths)) :
    sondes[i+1] = Sonde(sondes_paths[i])

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello Papa"}

@app.get("/temperature/{sonde_number}")
async def get_temp(sonde_number: int):
    sonde = sondes.get(sonde_number)
    if sonde :
        temperature = sonde.get_temperature()
        return {f"Temperature Sonde {sonde_number}" : temperature}
    else :
        return {f"Sonde not found"}
    
    

favicon_path = '/home/pi/Pictures/favicon.ico'

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)