from typing import Optional
from .common_options import CommonOptions
from .error_info import ErrorInfo
from .events import ConnectionEvent
from .states import ConnectionState


class ConnectionStateChange:
    def __init__(self, current: Optional[ConnectionState] = None, previous: Optional[ConnectionState] = None,
                 event: Optional[ConnectionEvent] = None, reason: Optional[ErrorInfo] = None):
        self.current = current
        self.previous = previous
        self.event = event
        self.reason = reason
