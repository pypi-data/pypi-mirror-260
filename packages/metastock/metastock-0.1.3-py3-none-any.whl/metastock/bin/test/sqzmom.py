from datetime import datetime, timedelta

from metastock.modules.com.technical_indicator.sqz_mom import SqzMom, SqzMomConfig
from metastock.modules.core.util.get_json_data import get_json_data

url = "http://localhost:3000/stock-price/history?code=BFC"
three_years_ago = datetime.now() - timedelta(days=3 * 365)
from_date = three_years_ago.strftime('%Y-%m-%d')
full_url = f"{url}&from={from_date}"
data = get_json_data(full_url)

sqz_config = SqzMomConfig()
sqz = SqzMom(data)
sqz.set_config(sqz_config)

sqzs = []

for i in range(10):
    date = data[i]['date']
    value, sqzOn, sqzOff, noSqz = sqz.set_date(date).get_data()
    sqzs.append(value)

print(sqzs)
