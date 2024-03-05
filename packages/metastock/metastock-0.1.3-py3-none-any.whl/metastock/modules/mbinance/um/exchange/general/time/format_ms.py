import arrow

from metastock.modules.mbinance.value.common import CommonValue


def format_ms(
    ms: int, time_format: str = "YYYY-MM-DD HH:mm:ss ZZ", timezone: bool = True
) -> str:
    if ms is None:
        return "None"

    arrow_time = arrow.get(ms / 1000)

    if timezone:
        arrow_tz = arrow_time.to(CommonValue.TIME_ZONE)

        return arrow_tz.format(time_format)

    return arrow_time.format(time_format)
