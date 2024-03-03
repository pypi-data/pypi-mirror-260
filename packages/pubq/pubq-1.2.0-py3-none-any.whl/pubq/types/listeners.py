from typing import Callable, Optional
from .channel import ChannelStateChange
from .connection import ConnectionStateChange
from .error_info import ErrorInfo
from .message import MessageObject

ConnectionListener = Callable[[ConnectionStateChange], None]
ChannelListener = Callable[[ChannelStateChange], None]
MessageListener = Callable[[MessageObject], None]
ErrorListener = Callable[[Optional[ErrorInfo]], None]
