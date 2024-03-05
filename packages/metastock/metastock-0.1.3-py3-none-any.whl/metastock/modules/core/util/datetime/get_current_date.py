import arrow


def get_current_date_string() -> str:
    current_time = arrow.now()

    # Định dạng thời gian theo định dạng YYYY-MM-DD
    formatted_time = current_time.format('YYYY-MM-DD')

    return formatted_time
