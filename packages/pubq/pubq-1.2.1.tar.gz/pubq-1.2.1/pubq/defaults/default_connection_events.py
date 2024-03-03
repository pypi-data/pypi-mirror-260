from typing import List

# Assuming that ConnectionEvent is a custom type alias defined in your code
ConnectionEvent = str

# Define DefaultConnectionEvents as a list of ConnectionEvent strings
DefaultConnectionEvents: List[ConnectionEvent] = [
    "initialized",
    "connecting",
    "connected",
    "disconnected",
    "suspended",
    "closing",
    "closed",
    "failed",
    "update",
]
