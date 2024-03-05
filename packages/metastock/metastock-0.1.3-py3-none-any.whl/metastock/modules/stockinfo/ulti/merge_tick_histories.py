import arrow

from metastock.modules.core.util.app_error import AppError


def group_by_time_period(entry, period_minutes=5):
    entry_time = arrow.get(entry["datetime"])
    rounded_minute = (entry_time.minute // period_minutes) * period_minutes
    rounded_time = entry_time.replace(minute=rounded_minute, second=0, microsecond=0)

    return rounded_time.format("YYYY-MM-DDTHH:mm:ss.SSSZ")


def _cal_grouped_tick_data(grouped_data, new_tick):
    pass


def merge_tick_histories(tick_histories: list, resolution: int = 5):
    tick_data = []
    for tick_day in tick_histories:
        date = arrow.get(tick_day["date"])
        date = date.to("Asia/Bangkok")
        meta = tick_day["meta"]
        if isinstance(meta, list):
            for tick in meta:
                time_string = tick["time"]

                current_datetime = date.replace(
                    hour=int(time_string.split(":")[0]),
                    minute=int(time_string.split(":")[1]),
                    second=int(time_string.split(":")[2]),
                )

                datetime_str = current_datetime.format("YYYY-MM-DDTHH:mm:ss.SSSZ")
                # datetime = arrow.get(datetime_str)
                # print(datetime_str)
                tick_data.append({"datetime": datetime_str, **tick})

    group_by_res = {}
    if resolution not in [1, 5, 15, 30]:
        raise AppError(f"Not support resolution {resolution}")

    for tick in tick_data:
        rounded_time = group_by_time_period(tick, resolution)
        p = tick["p"]
        if rounded_time in group_by_res:
            grouped_data = group_by_res.get(rounded_time)
            if grouped_data["high"] < p:
                grouped_data["high"] = p

            if grouped_data["low"] > p:
                grouped_data["low"] = p

            grouped_data["close"] = p
            grouped_data["num"] += 1
            grouped_data["vol"] += tick["vol"]

        else:
            group_by_res[rounded_time] = {
                "date": rounded_time,
                "open": p,
                "high": p,
                "low": p,
                "close": p,
                "num": 1,
                "vol": tick["vol"],
            }

    return sorted(list(group_by_res.values()), key=lambda x: x["date"], reverse=True)
