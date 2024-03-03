from typing import Optional


class PrivateOptions:
    def __init__(self, secure: bool, path: str, hostname: Optional[str] = None, port: Optional[int] = None):
        self.secure = secure
        self.path = path
        self.hostname = hostname
        self.port = port
