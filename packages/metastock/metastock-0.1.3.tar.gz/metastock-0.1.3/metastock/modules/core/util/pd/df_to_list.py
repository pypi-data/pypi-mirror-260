import pandas as pd

from metastock.modules.core.util.datetime.datetime_to_str import datetime_to_str


def df_to_list(df: pd.DataFrame, index_name='date'):
    return [
        {**row.to_dict(), index_name: datetime_to_str(index)}
        for index, row in df.iterrows()
    ]
