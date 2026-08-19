class ApiKeyError(Exception):
    def __init__(self, message):
        self.type = "API Key Error"
        self.status_code = "401"
        self.message = message