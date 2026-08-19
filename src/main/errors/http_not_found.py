class NotFoundError(Exception):
    def __init__(self, message):
        self.type = "Not Found"
        self.status_code = "404"
        self.message = message