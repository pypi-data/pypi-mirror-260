import pandas as pd


def pd_to_datetime(date: str | pd.Series):
    return pd.to_datetime(date, utc=True)
