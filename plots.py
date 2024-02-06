import datetime

import pandas as pd
import plotly.graph_objects as go
from starlette.responses import HTMLResponse

from config import data_path
from server import app


@app.get("/plot")
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

    # Show the figure
    fig.to_html()
    plot_div = fig.to_html(full_html=False)

    # Embed the plot div in an HTML response
    html_content = f"""
    <html>
        <head>
            <title>Saint Paër chauffage</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        </head>
        <body>
            <h1>Saint Paër chauffage</h1>
            {plot_div}
        </body>
    </html>
    """

    return HTMLResponse(content=html_content)


@app.get("/plot/external")
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
