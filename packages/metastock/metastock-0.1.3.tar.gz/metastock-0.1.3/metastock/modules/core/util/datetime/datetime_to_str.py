from datetime import datetime

import arrow


def datetime_to_str(dt):
    if isinstance(dt, datetime):
        return arrow.get(dt).format('YYYY-MM-DD')

    return 'could_not_parse_datetime'
