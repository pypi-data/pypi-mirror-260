from typing import Optional, Any
from .types.message import MessageObject


class Message:
    def __init__(self, msg: Optional[MessageObject] = None):
        self.id = msg.id if (msg and hasattr(msg, 'id')) else None
        self.clientId = msg.clientId if (
            msg and hasattr(msg, 'clientId')) else None
        self.connectionId = msg.connectionId if (
            msg and hasattr(msg, 'connectionId')) else None
        self.data = msg.data if hasattr(msg, 'data') else None

    def toObject(self) -> dict:
        obj = {}

        if self.id is not None:
            obj['id'] = self.id
        if self.clientId is not None:
            obj['clientId'] = self.clientId
        if self.connectionId is not None:
            obj['connectionId'] = self.connectionId
        if self.data is not None:
            obj['data'] = self.data

        return obj
