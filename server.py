import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sonde import sondes
from config import favicon_path
from fastapi.responses import FileResponse

import datetime
import csv
from easycharts import ChartServer
from easyschedule import EasyScheduler

logger = logging.getLogger("server")
scheduler = EasyScheduler()


def open_last_n_rows(file_path, n):
    with open(file_path, "r") as file:
        return file.readlines()[-n:]


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Running server")
    scheduler.start()
    app.charts = await ChartServer.create(
        app,
        charts_db="charts_database",
        chart_prefix='/mycharts'
    )
    await app.charts.create_dataset(
        'ext_temperature',
        labels=[],
        datasets=[],
    )
    await app.charts.create_dataset(
        'out_temperature',
        labels=[],
        datasets=[],

    )
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


@app.get("/last_n_lines")
async def test_n_lines():
    time_now = datetime.datetime.now().isoformat()[11:19]
    data = open_last_n_rows("/home/pi/Documents/raspberry_heating/data/2024-02-04.csv", 30)
    csv_reader = csv.reader(data, delimiter=',')
    lines = [(line[0], line[1], line[2]) for line in csv_reader]
    dates = [line[0] for line in lines]
    output_temperatures = [line[1] for line in lines]
    external_temperatures = [line[2] for line in lines]
    for i in range(len(dates)):
        await app.charts.update_dataset(
            'ext_temperature',
            label=dates[i],
            data=external_temperatures[i]
        )
        await app.charts.update_dataset(
            'out_temperature',
            label=dates[i],
            data=output_temperatures[i]
        )
