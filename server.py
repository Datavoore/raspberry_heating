import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.logger import logger
from sonde import sondes
from config import favicon_path
from fastapi.responses import FileResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Running server")
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


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)
