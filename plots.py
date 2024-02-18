import datetime

import pandas as pd
import plotly.graph_objects as go
from fastapi import APIRouter
from starlette.responses import HTMLResponse

from config import data_path

plot_router = APIRouter(prefix="/plot", tags=["plot"])


def load_csv(date):
    temps_df = pd.read_csv(
        data_path + f"{date}.csv",
        names=(
            "time",
            "temperature_out",
            "external_temperature",
            "wanted_temperature",
            "control",
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


@plot_router.get("/")
async def plot(date: str = None):
    if date is None:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
    temps_df = load_csv(date)
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


@plot_router.get("/external")
async def plot(date: str = None):
    if date is None:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
    temps_df = pd.read_csv(
        data_path + f"{date}.csv",
        names=(
            "time",
            "temperature_out",
            "external_temperature",
            "wanted_temperature",
            "control",
        ),
        header=None,
        sep=",",
    )
    temps_df["parsed_datetime"] = pd.to_datetime(temps_df["time"])
    # Create a bar trace for control values with increased transparency

    # Create a line trace for temperature values
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
    fig.to_html()
    plot_div = fig.to_html(full_html=False)

    # Embed the plot div in an HTML response
    html_content = f"""
    <html>
        <head>
            <title>Saint Paër température extérieure</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        </head>
        <body>
            <h1>Saint Paër température extérieure</h1>
            {plot_div}
        </body>
    </html>
    """

    return HTMLResponse(content=html_content)
