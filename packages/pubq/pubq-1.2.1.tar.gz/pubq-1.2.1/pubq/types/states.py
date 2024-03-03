from enum import Enum


class ConnectionState(Enum):
    INITIALIZED = "initialized"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    SUSPENDED = "suspended"
    CLOSING = "closing"
    CLOSED = "closed"
    FAILED = "failed"


class ChannelState(Enum):
    INITIALIZED = "initialized"
    SUBSCRIBING = "subscribing"
    SUBSCRIBED = "subscribed"
    UNSUBSCRIBING = "unsubscribing"
    UNSUBSCRIBED = "unsubscribed"
    SUSPENDED = "suspended"
    FAILED = "failed"
