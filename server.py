import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from pydantic import BaseModel

from command_override_utils import set_command_override, get_command_override
from probe import probes
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

# Mount the 'ui' directory as a static directory
app.mount("/ui", StaticFiles(directory="ui"), name="ui")


# Route to serve the home.html file
@app.get("/")
async def get_home():
    return FileResponse("ui/home.html")


app.include_router(plot_router)


@app.get("/temperature/{probe_number}")
async def get_temp(probe_number: int):
    probe = probes.get(probe_number)
    if probe:
        temperature = probe.get_temperature()
        return {"Temperature Probe": temperature}
    else:
        return {"Probe not found"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("ui/heating.png")

# Pydantic model for the request body
class SetCommandRequest(BaseModel):
    value: int

# Endpoint to get the current command override
@app.get("/command-override")
async def get_command_override_route():
    current_value = get_command_override()
    if current_value is None:
        # Indicate that the value is not set or couldn't be read
         return {"command_override": None} # Or a specific error structure
    return {"command_override": current_value}

# Endpoint to set the command override
@app.post("/command-override")
async def set_command(request: SetCommandRequest):
    success = set_command_override(request.value)
    return {"status": "success", "new_value": request.value}
