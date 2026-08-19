class HttpBadRequestError(Exception):
    def __init__(self, message):
        self.type = "Bad Request"
        self.status_code = "400"
        self.message = message
