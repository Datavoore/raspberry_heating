import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from sonde import sondes
from config import favicon_path
from fastapi.responses import FileResponse
from plots import plot_router

logger = logging.getLogger("server")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Running server")
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(plot_router)


@app.get("/temperature/{sonde_number}")
async def get_temp(sonde_number: int):
    sonde = sondes.get(sonde_number)
    if sonde:
        temperature = sonde.get_temperature()
        return {f"Température Sonde {sonde_number}": temperature}
    else:
        return {f"Sonde not found"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)
