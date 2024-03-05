class MBinanceError(Exception):
    def __init__(self, message="Error", code="M_BINANCE_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)

    def get_message(self):
        return self.message

    def get_code(self):
        return self.code
