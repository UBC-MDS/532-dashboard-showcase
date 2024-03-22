from dash import Dash, Input, Output, callback, dcc, html
import altair as alt
import dash_vega_components as dvc
import plotly.express as px
import json
from pathlib import Path

print('\n'.join([str(x) for x in sorted(Path.cwd().iterdir())]))

df = px.data.tips()
chart = (
    alt.Chart(df)
    .mark_circle(size=50)
    .encode(x="tip", y="total_bill")
    .add_params(
        alt.selection_point(
            fields=["tip", "total_bill"], name="selected_points", on="mouseover"
        )
    )
)


app = Dash(__name__)
app.layout = html.Div(
    [
        html.H1("Interact with Click Data"),
        dvc.Vega(
            id="chart", signalsToObserve=["selected_points"], spec=chart.to_dict()
        ),
        dcc.Markdown(id="chart-params"),
    ]
)
server=app.server


@callback(
    Output("chart-params", "children"),
    Input("chart", "signalData"),
    prevent_initial_call=True,
)
def display_altair_width_params(params):
    return "```json\n" + json.dumps(params, indent=2) + "\n```"


if __name__ == "__main__":
    app.run_server(debug=True)

