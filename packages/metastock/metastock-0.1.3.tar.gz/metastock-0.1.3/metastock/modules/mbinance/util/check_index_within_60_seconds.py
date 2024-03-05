from metastock.modules.core.util.environment import is_development


def check_index_within_60_seconds(df):
    # Kiểm tra nếu DataFrame rỗng
    if not is_development() or df.empty:
        return True

    # Lấy danh sách các chỉ số (index)
    indexes = df.index.tolist()
    indexes.reverse()
    # Lặp qua danh sách chỉ số để kiểm tra khoảng cách giữa chúng
    for i in range(1, len(indexes)):
        time_diff = indexes[i] - indexes[i - 1]
        if time_diff != 60 * 1000:
            return False

    # Nếu không có chỉ số nào có khoảng cách lớn hơn 60 giây, trả về True
    return True
