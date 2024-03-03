from typing import List

# Assuming that ChannelEvent is a custom type alias defined in your code
ChannelEvent = str

# Define DefaultChannelEvents as a list of ChannelEvent strings
DefaultChannelEvents: List[ChannelEvent] = [
    "initialized",
    "subscribing",
    "subscribed",
    "unsubscribing",
    "unsubscribed",
    "suspended",
    "failed",
    "update",
]
