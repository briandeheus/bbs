class BBSException(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.msg = message
