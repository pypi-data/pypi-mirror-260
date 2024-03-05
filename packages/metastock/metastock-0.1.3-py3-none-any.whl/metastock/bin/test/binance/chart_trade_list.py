import arrow
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
from plotly.subplots import make_subplots
from sqlalchemy import and_

from metastock.modules.com.util.price.wma import wma
from metastock.modules.core.db.postgres_manager import postgres_manager
from metastock.modules.core.util.environment import config_env
from metastock.modules.mbinance.um.db.models import BinanceTrade
from metastock.modules.mbinance.value.common import CommonValue

config_env("BN")
postgres_manager.initialize()
session = postgres_manager.get_session()

data = (
    session.query(BinanceTrade)
    .filter(and_(BinanceTrade.was_buyer_maker == False))
    .order_by(BinanceTrade.timestamp.desc())
    .limit(5000)
)

# df = pd.DataFrame.from_records([trade.__dict__ for trade in data])

df = pd.read_sql_query(sql=data.statement, con=postgres_manager.get_engine())
df["timestamp"] = df["timestamp"].apply(
    lambda x: arrow.get(x / 1000).to(CommonValue.TIME_ZONE).datetime
)
df.set_index("timestamp", inplace=True)
df = df[df["price"] != df["price"].shift()]
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
            x=df.index,
            y=df["price"],  # replace with your own data source
            name="price",
        ),
        secondary_y=False,
    )
    length = 10
    source = df["price"]
    # source = source.iloc[::-1]
    hulma = wma(
        2 * wma(source, int(length / 2)) - wma(source, length),
        round(np.sqrt(length)),
    )

    fig.add_trace(
        go.Scatter(x=hulma.index, y=hulma, name="hullma"),
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
