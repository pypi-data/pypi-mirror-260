import pandas as pd
import arrow

from metastock.modules.core.logging.logger import Logger
from metastock.modules.core.util.get_json_data import get_json_data
from metastock.modules.core.util.http_client import http_client


def convert_to_ict(timestamp):
    return arrow.get(timestamp).to('Asia/Ho_Chi_Minh').format('HH:mm:ss')


try:
    url = "https://api.simplize.vn/api/historical/ticks/TCB"
    response = http_client().get(url)

    json_data = response.json()
    columns = ["datetime", "volume", "price", "action"]

    df = pd.DataFrame(json_data.get('data'), columns = columns)
    df["datetime"] = df["datetime"].apply(convert_to_ict)

    total_khoi_luong_B = df[df["action"] == "B"][df["volume"] > 10000]["volume"].sum()
    total_khoi_luong_S = df[df["action"] == "S"][df["volume"] > 10000]["volume"].sum()
    Logger().info(df[df["action"] == "B"][df["volume"] > 10000])
    Logger().info(f"Khoi luong Mua {total_khoi_luong_B}")
    Logger().info(f"Khoi luong Ban {total_khoi_luong_S}")
except Exception as e:
    Logger().error("An error occurred: %s", e, exc_info = True)
