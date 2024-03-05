import csv
import os


class CsvWriter:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def check_data_format(self, header, data):
        """
        Kiểm tra xem dữ liệu mới có đúng định dạng với header đã có hay không.
        """
        return set(header) == set(data.keys())

    def write_to_csv(self, data):
        """
        Ghi dữ liệu vào tệp CSV, kiểm tra và thêm tiêu đề nếu cần.
        """
        # Kiểm tra xem tệp CSV đã tồn tại hay chưa
        file_exists = os.path.isfile(self.file_path)

        # Mở tệp CSV để ghi
        with open(self.file_path, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())

            # Nếu tệp không tồn tại hoặc chưa có tiêu đề, ghi tiêu đề vào
            if not file_exists or file.tell() == 0:
                writer.writeheader()

            # Kiểm tra và ghi dữ liệu mới vào
            for row in data:
                if not self.check_data_format(writer.fieldnames, row):
                    print("Error: Data format does not match header format!")
                    return False
                writer.writerow(row)

        return True
