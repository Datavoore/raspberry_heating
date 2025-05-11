import datetime

import pandas as pd
import plotly.graph_objects as go
from fastapi import APIRouter
from starlette.responses import HTMLResponse

from config import data_path

plot_router = APIRouter(prefix="/plot", tags=["plot"])
timedeltas = {"30m": datetime.timedelta(minutes=30), "3h": datetime.timedelta(hours=3)}
date_format = "%Y-%m-%d"


def get_filtered_csv(date, subset):
    now = datetime.datetime.now()
    if date is None:
        date = now.strftime(date_format)
    temps_df = load_csv(date)
    if subset and subset in timedeltas:
        timedelta = timedeltas[subset]
        temps_df = temps_df[temps_df["parsed_datetime"] >= now - timedelta]
    return temps_df


def load_csv(date):
    temps_df = pd.read_csv(
        data_path + f"{date}.csv",
        names=(
            "time",
            "temperature_out",
            "external_temperature",
            "wanted_temperature",
            "control",
            "command"
        ),
        header=None,
        sep=",",
    )
    temps_df["parsed_datetime"] = pd.to_datetime(temps_df["time"])
    return temps_df


def get_main_graph(temps_df):
    # Create a bar trace for control values with increased transparency
    trace3 = go.Bar(
        x=temps_df["parsed_datetime"],
        y=temps_df["control"],
        name="Control",
        yaxis="y2",
        marker=dict(color="rgba(255, 0, 0, 0.3)"),
    )

    # Create a line trace for temperature values
    trace1 = go.Scatter(
        x=temps_df["parsed_datetime"],
        y=temps_df["temperature_out"],
        mode="lines",
        name="Température eau",
    )
    trace2 = go.Scatter(
        x=temps_df["parsed_datetime"],
        y=temps_df["wanted_temperature"],
        mode="lines",
        name="Température souhaitée",
    )

    # Create layout with two y-axes
    layout = go.Layout(
        title="Température eau et température souhaitée",
        yaxis=dict(title="Température"),
        yaxis2=dict(title="Control", overlaying="y", side="right"),
    )

    # Create a figure with the defined traces and layout
    fig = go.Figure(data=[trace3, trace1, trace2], layout=layout)

    plot_div = fig.to_html(full_html=False)
    return plot_div


def get_external_temperature_graph(temps_df):
    trace1 = go.Scatter(
        x=temps_df["parsed_datetime"],
        y=temps_df["external_temperature"],
        mode="lines",
        name="Température extérieure",
    )

    # Create layout with two y-axes
    layout = go.Layout(
        title="Température extérieure",
        yaxis=dict(title="Température"),
    )

    # Create a figure with the defined traces and layout
    fig = go.Figure(data=[trace1], layout=layout)

    # Show the figure
    plot_div = fig.to_html(full_html=False)
    return plot_div


@plot_router.get("/")
async def plot(date: str = None, subset: str = None):
    temps_df = get_filtered_csv(date, subset)
    plot_div = get_main_graph(temps_df)

    # Embed the plot div in an HTML response
    html_content = f"""
    <html>
        <head>
            <title>Chauffage Saint Paër {date}</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        </head>
        <body>
            <h1>Chauffage Saint Paër {date}</h1>
            {plot_div}
        </body>
    </html>
    """

    return HTMLResponse(content=html_content)


@plot_router.get("/yesterday")
async def plot_yesterday():
    date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime(date_format)
    return await plot(date)


@plot_router.get("/external")
async def plot_external(date: str = None, subset: str = None):
    temps_df = get_filtered_csv(date, subset)
    plot_div = get_external_temperature_graph(temps_df)

    html_content = f"""
    <html>
        <head>
            <title>Saint Paër température extérieure {date}</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        </head>
        <body>
            <h1>Saint Paër température extérieure {date}</h1>
            {plot_div}
        </body>
    </html>
    """

    return HTMLResponse(content=html_content)
