import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.responses import HTMLResponse

from sonde import sondes
from config import favicon_path, data_path
from fastapi.responses import FileResponse
import pandas as pd
import plotly.graph_objects as go

logger = logging.getLogger("server")


def open_last_n_rows(file_path, n):
    with open(file_path, "r") as file:
        return file.readlines()[-n:]


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


@app.get("/plot")
async def plot():
    temps_df = pd.read_csv(data_path + "2024-02-04.csv",
                           names=("time", "temperature_out", "external_temperature", "wanted_temperature", "control"),
                           header=None, sep=",")
    temps_df["parsed_datetime"] = pd.to_datetime(temps_df["time"])
        # Convert the Plotly figure to an HTML div
    # Create a bar trace for control values with increased transparency
    trace3 = go.Bar(
        x=temps_df["parsed_datetime"],
        y=temps_df["control"],
        name="Control",
        yaxis="y2",
        marker=dict(color="rgba(255, 0, 0, 0.3)")
    )

    # Create a line trace for temperature values
    trace1 = go.Scatter(x=temps_df["parsed_datetime"], y=temps_df["temperature_out"], mode="lines",
                        name="Temperature Out")
    trace2 = go.Scatter(x=temps_df["parsed_datetime"], y=temps_df["wanted_temperature"], mode="lines",
                        name="Wanted Temperature")

    # Create layout with two y-axes
    layout = go.Layout(
        title="Temperature and Control Comparison",
        yaxis=dict(title="Temperature"),
        yaxis2=dict(title="Control", overlaying="y", side="right"),
    )

    # Create a figure with the defined traces and layout
    fig = go.Figure(data=[trace3, trace1, trace2], layout=layout)

    # Show the figure
    fig.to_html()
    plot_div = fig.to_html(full_html=False)

    # Embed the plot div in an HTML response
    html_content = f"""
    <html>
        <head>
            <title>Interactive Temperature and Control Plot</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        </head>
        <body>
            <h1>Interactive Temperature and Control Plot</h1>
            {plot_div}
        </body>
    </html>
    """

    return HTMLResponse(content=html_content)
