from typing import Optional
from .error_info import ErrorInfo
from .events import ChannelEvent
from .states import ChannelState


class ChannelStateChange:
    def __init__(self, current: Optional[ChannelState] = None, previous: Optional[ChannelState] = None,
                 event: Optional[ChannelEvent] = None, reason: Optional[ErrorInfo] = None):
        self.current = current
        self.previous = previous
        self.event = event
        self.reason = reason
