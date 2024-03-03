from typing import Optional, Any


class MessageObject:
    def __init__(self, id: Optional[str] = None, clientId: Optional[str] = None, connectionId: Optional[str] = None,
                 data: Optional[Any] = None):
        self.id = id
        self.clientId = clientId
        self.connectionId = connectionId
        self.data = data
