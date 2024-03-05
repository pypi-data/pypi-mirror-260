import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
from plotly.subplots import make_subplots


app = Dash(__name__)


app.layout = html.Div(
    [
        html.H4("Interactive data-scaling using the secondary axis"),
        html.P("Select red line's Y-axis:"),
        dcc.RadioItems(id="radio", options=["Primary", "Secondary"], value="Secondary"),
        dcc.Graph(id="graph"),
    ]
)


@app.callback(Output("graph", "figure"), Input("radio", "value"))
def display_(radio_value):
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(
            x=[1, 2, 3],
            y=[40, 50, 60],  # replace with your own data source
            name="yaxis data",
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=[1, 2, 3], y=[14, 5, 6], name="yaxis2 data"),
        secondary_y=radio_value == "Secondary",
    )

    # Add figure title
    fig.update_layout(title_text="Double Y Axis Example")

    # Set x-axis title
    fig.update_xaxes(title_text="xaxis title")

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>primary</b> yaxis title", secondary_y=False)
    fig.update_yaxes(title_text="<b>secondary</b> yaxis title", secondary_y=True)

    return fig


app.run_server(debug=True)
