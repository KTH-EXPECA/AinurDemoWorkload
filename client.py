import time
from dataclasses import dataclass
from typing import List, Optional

import click
import numpy as np
import numpy.typing as npt
import plotly.express as px
import requests
from dash import Dash, Input, Output, dcc, html
from sklearn import datasets

# constants
rng = np.random.default_rng()
data, _ = datasets.load_digits(return_X_y=True)
app = Dash(__name__)


@dataclass
class AppState:
    current_sample: npt.NDArray


app_state = AppState(current_sample=rng.choice(data))

app.layout = html.Div(
    children=[
        html.Div(id="hidden-div", style={"display": None}),
        html.Header("Sample:"),
        dcc.Graph(id="image", config={"staticPlot": True}),
        html.Div(
            children=[
                html.Button(id="reload", children=["New Sample"]),
                html.Button(id="submit", children=["Submit to classifier backend"]),
            ]
        ),
        html.P(),
        html.Div("Results:"),
        html.Div(
            id="results",
            style={"backgroundColor": "#eaeaea"},
            children=[
                html.Div(children=["Label: ", "3"]),
                html.Div(children=["Confidence: ", "0.87"]),
                html.P(),
                html.Div(children=["RTT: ", "247 ms"]),
                html.Div(children=["Processing Time: ", "200 ms"]),
                html.Div(children=["Network Time: ", "47 ms"]),
            ],
        ),
    ]
)


# callback to change the image
@app.callback(
    Output(component_id="image", component_property="figure"),
    Input(component_id="reload", component_property="n_clicks"),
)
def new_sample(*args, **kwargs) -> html.Figure:
    sample = rng.choice(data)
    app_state.current_sample = sample
    fig = px.imshow(sample.reshape((8, 8)), color_continuous_scale="greys")
    fig.update(layout_coloraxis_showscale=False)
    return fig


@click.command()
@click.argument("server-addr", type=str)
@click.option(
    "-p",
    "--server-port",
    type=click.IntRange(0, 65535),
    default=80,
    show_default=True,
)
def main(server_addr: str, server_port: int) -> None:
    # new_sample()

    @app.callback(
        Output(component_id="results", component_property="children"),
        Input(component_id="submit", component_property="n_clicks"),
    )
    def submit(n_clicks: Optional[int]) -> List:
        if n_clicks is not None:
            ti = time.monotonic()
            res = requests.post(
                url=f"http://{server_addr}:{server_port}/classify",
                data=app_state.current_sample.tobytes(),
                headers={"Content-Type": "application/octet-stream"},
            )
            dt = time.monotonic() - ti
            results = res.json()
            proc_time = results["time"]

            return [
                html.Div(children=["Label: ", results["label"]]),
                html.Div(children=["Confidence: ", results["confidence"]]),
                html.P(),
                html.Div(children=["RTT: ", f"{dt * 1000:0.3f} ms"]),
                html.Div(children=["Processing Time: ", f"{proc_time * 1000:0.3f} ms"]),
                html.Div(
                    children=[
                        "Network Time: ",
                        f"{(dt - proc_time) * 1000:0.3f} ms",
                    ]
                ),
            ]

    app.run(host="0.0.0.0", port=8080, debug=True)


if __name__ == "__main__":
    main()
