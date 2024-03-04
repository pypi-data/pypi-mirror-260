class AioHttpRequestError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class BithumbPublicError(AioHttpRequestError):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class BithumbPrivateError(AioHttpRequestError):
    def __init__(self, message):
        self.message = message
        super().__init__(message)