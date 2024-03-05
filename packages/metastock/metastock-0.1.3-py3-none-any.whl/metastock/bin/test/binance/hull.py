import arrow
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
from plotly.subplots import make_subplots

from metastock.modules.core.db.postgres_manager import postgres_manager
from metastock.modules.core.util.environment import config_env
from metastock.modules.mbinance.um.db.models import Candlestick
from metastock.modules.mbinance.um.trade.strategy.hull import (
    get_hull_status,
    get_hull_from_kline,
)
from metastock.modules.mbinance.value.common import CommonValue

config_env("BN")
postgres_manager.initialize()
session = postgres_manager.get_session()

data = (
    session.query(Candlestick).order_by(Candlestick.open_time.desc())
    # .filter(and_(BinanceTrade.was_buyer_maker == False))
    .limit(500)
)

# df = pd.DataFrame.from_records([trade.__dict__ for trade in data])

df = pd.read_sql_query(sql=data.statement, con=postgres_manager.get_engine())
df["open_time"] = df["open_time"].apply(
    lambda x: arrow.get(x / 1000).to(CommonValue.TIME_ZONE).datetime
)
df.set_index("open_time", inplace=True)

hulma = get_hull_from_kline(df)

hull_status = get_hull_status(hulma)

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
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=hulma.index, y=hulma, name="hullma"),
        secondary_y=False,
    )
    return fig


app.run_server(debug=True)
