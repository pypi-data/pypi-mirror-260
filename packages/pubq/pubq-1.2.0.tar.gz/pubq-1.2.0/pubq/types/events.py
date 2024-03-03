from enum import Enum


class ConnectionEvent(Enum):
    INITIALIZED = "initialized"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    SUSPENDED = "suspended"
    CLOSING = "closing"
    CLOSED = "closed"
    FAILED = "failed"
    UPDATE = "update"


class ChannelEvent(Enum):
    INITIALIZED = "initialized"
    SUBSCRIBING = "subscribing"
    SUBSCRIBED = "subscribed"
    UNSUBSCRIBING = "unsubscribing"
    UNSUBSCRIBED = "unsubscribed"
    SUSPENDED = "suspended"
    FAILED = "failed"
    UPDATE = "update"
