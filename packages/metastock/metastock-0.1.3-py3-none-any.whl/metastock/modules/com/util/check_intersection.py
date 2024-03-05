def check_intersection(line1, line2):
    a, b = line1
    c, d = line2

    # Kiểm tra nếu một trong các đầu của đoạn thẳng thứ nhất nằm giữa đoạn thẳng thứ hai
    if (c <= a <= d) or (c <= b <= d) or (a <= c <= b) or (a <= d <= b):
        return True
    else:
        return False
