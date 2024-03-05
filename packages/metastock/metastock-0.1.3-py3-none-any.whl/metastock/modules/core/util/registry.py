class Registry(object):
    __data = {}

    def set_data(self, key: str, val):
        self.__data[key] = val

        return self

    def get_data(self, key: str):
        return self.__data.get(key)

    def has_data(self, key: str):
        return key in self.__data


registry = Registry()
