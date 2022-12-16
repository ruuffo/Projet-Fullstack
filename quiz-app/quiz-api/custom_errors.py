# Custom Exception
class CustomError(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

    def __str__(self):
        return "Exception : " + repr(self.code) + "\n" + self.message
