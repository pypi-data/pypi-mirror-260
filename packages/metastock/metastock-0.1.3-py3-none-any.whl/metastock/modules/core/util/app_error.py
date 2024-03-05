class AppError(Exception):
    def __init__(self, message='AppError message', code='app_error_000'):
        self.message = message
        self.code = code
        super().__init__(message)

    def get_message(self):
        return self.message

    def get_code(self):
        return self.code
