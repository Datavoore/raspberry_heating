import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.background import BackgroundTask

from GPIO import *
from heating_controller import HeatingController, Valve
from sonde import sondes
from config import favicon_path
from fastapi.responses import FileResponse
from fastapi import BackgroundTasks

heating_controller = HeatingController(sondes[2], None, Valve(relay_lower_pin_num, relay_raise_pin_num), 50)


def run_main_loop():
    while True:
        heating_controller.update()
        asyncio.sleep(40)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize heater controller and run background tasks
    asyncio.run(run_main_loop())
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/temperature/{sonde_number}")
async def get_temp(sonde_number: int):
    sonde = sondes.get(sonde_number)
    if sonde:
        temperature = sonde.get_temperature()
        return {f"Temperature Sonde {sonde_number}": temperature}
    else:
        return {f"Sonde not found"}

@app.get("/temperature")
async def get_temp():
    return {f"Temperature Sonde": heating_controller.get_output_temperature()}

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)
