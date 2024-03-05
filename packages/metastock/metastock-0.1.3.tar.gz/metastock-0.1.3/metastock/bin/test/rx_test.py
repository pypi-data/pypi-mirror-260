# import pandas as pd
#
# data = [
#     {"name": "Alice", "age": 25, "city": "New York"},
#     {"name": "Bob", "age": 30, "city": "Paris"},
#     {"name": "Charlie", "age": 35, "city": "London"},
#     {"name": "Charlie1", "age": 35, "city": "London"},
#     {"name": "Charlie2", "age": 35, "city": "London"},
#     {"name": "Charlie3", "age": 35, "city": "London"},
#     {"name": "Charlie4", "age": 35, "city": "London"},
# ]
#
# # Tạo DataFrame chỉ với các cột được chọn
# # Giả sử bạn chỉ muốn giữ lại cột 'name' và 'city'
# df = pd.DataFrame(data, columns=["name", "city"])
# subset = df.iloc[5:3]
# print(subset)

from itertools import product

for combine in product(range(1, 3), range(4, 6), range(7, 9)):
    print(*combine)
