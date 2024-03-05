from datetime import datetime, timedelta

from metastock.modules.core.util.get_json_data import get_json_data


def get_history_data(symbol: str, year: int = 2):
    url = f"http://localhost:3000/stock-price/history?code={symbol}"
    three_years_ago = datetime.now() - timedelta(days = year * 365)
    from_date = three_years_ago.strftime('%Y-%m-%d')
    full_url = f"{url}&from={from_date}"
    return get_json_data(full_url)
