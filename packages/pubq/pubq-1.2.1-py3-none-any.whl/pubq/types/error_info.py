from typing import Optional


class ErrorInfo:
    def __init__(self, code: Optional[int] = None, statusCode: Optional[int] = None, message: Optional[str] = None,
                 cause: Optional[Exception] = None, href: Optional[str] = None):
        self.code = code
        self.statusCode = statusCode
        self.message = message
        self.cause = cause
        self.href = href
