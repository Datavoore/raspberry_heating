import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from probe import probes
from config import favicon_path
from fastapi.responses import FileResponse
from plots import plot_router

logger = logging.getLogger("server")


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(plot_router)


@app.get("/temperature/{probe_number}")
async def get_temp(probe_number: int):
    probe = probes.get(probe_number)
    if probe:
        temperature = probe.get_temperature()
        return {f"Temperature Probe": temperature}
    else:
        return {f"Probe not found"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)
