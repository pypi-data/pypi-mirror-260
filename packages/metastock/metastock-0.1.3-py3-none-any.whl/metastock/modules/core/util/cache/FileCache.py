import os

import cachetools


# Tạo một custom cache file
class FileCache(cachetools.Cache):
    def __init__(self, cache_filename="default_cache", maxsize=128):
        super(FileCache, self).__init__(maxsize)
        self.cache_filename = cache_filename

    def __contains__(self, key):
        return os.path.exists(self.get_cache_filename(key))

    def __getitem__(self, key):
        try:
            with open(self.get_cache_filename(key), "r") as file:
                return file.read()
        except FileNotFoundError:
            raise KeyError(key)

    def __setitem__(self, key, value):
        with open(self.get_cache_filename(key), "w") as file:
            file.write(value)

    def __delitem__(self, key):
        try:
            os.remove(self.get_cache_filename(key))
        except FileNotFoundError:
            pass

    def get_cache_filename(self, key):
        # Tạo tên file cache dựa trên key
        return f"{self.cache_filename}_{key}"


# Khởi tạo một custom FileCache với tên file cache và kích thước tùy chọn
# cache_manager = FileCache("my_cache", maxsize=100)

# Sử dụng cache_manager như một cache bình thường
# cache_manager["my_key"] = "my_value"
# value = cache_manager["my_key"]

# Bạn có thể sử dụng cache_manager trong decorator hoặc function tùy ý
