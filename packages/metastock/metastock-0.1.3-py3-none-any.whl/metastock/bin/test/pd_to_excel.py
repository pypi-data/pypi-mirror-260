import pandas as pd

# Tạo DataFrame mẫu
data = {
    "Name": ["John", "Anna", "Peter", "Linda"],
    "Age": [28, 35, 25, 41],
    "City": ["New York", "Paris", "Berlin", "London"],
}
df = pd.DataFrame(data)

# Tên file Excel đích
excel_file = "example.xlsx"

with pd.ExcelWriter("path_to_file.xlsx") as writer:
    # Khởi tạo một đối tượng Pandas ExcelWriter
    # writer = pd.ExcelWriter(excel_file, engine="xlsxwriter")

    # Ghi DataFrame vào Excel
    df.to_excel(writer, index=False, sheet_name="Sheet1")

    # Lấy đối tượng workbook từ writer
    workbook = writer.book
    # worksheet = workbook.add_worksheet()
    # Lấy đối tượng worksheet từ writer
    # worksheet = writer.sheets["Sheet1"]

    # Tạo một đối tượng định dạng để định dạng header
    # header_format = workbook.add_format(
    #     {"bold": True, "bg_color": "#F0F0F0", "font_color": "black", "border": 1}
    # )
    #
    # # Áp dụng định dạng cho header (tất cả các cột)
    # for col_num, value in enumerate(df.columns.values):
    #     worksheet.write(0, col_num, value, header_format)
    #
    # # Tạo một đối tượng định dạng để định dạng dòng
    # row_format = workbook.add_format(
    #     {"bold": True, "bg_color": "yellow", "font_color": "black", "border": 1}
    # )
    #
    # # Áp dụng định dạng cho một số dòng cụ thể (ví dụ: dòng thứ 2)
    # row_index = 2
    # for col_num, value in enumerate(df.columns.values):
    #     worksheet.write(row_index, col_num, df.columns.values[col_num], row_format)
