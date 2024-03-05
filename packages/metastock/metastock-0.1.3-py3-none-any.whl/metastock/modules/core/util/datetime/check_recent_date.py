import arrow


def check_recent_date(date_str: str, recent: int = 3) -> bool:
    # Chuyển chuỗi ngày thành đối tượng arrow
    input_date = arrow.get(date_str, 'YYYY-MM-DD')

    # Lấy ngày hiện tại
    current_date = arrow.now()

    # Tính khoảng cách giữa ngày đầu vào và ngày hiện tại
    delta = (current_date - input_date).days

    # Kiểm tra xem ngày đầu vào có nằm trong vòng 3 ngày gần đây hay không
    if 0 <= delta <= recent:
        return True
    else:
        return False
