from .types.connection import ConnectionState, ConnectionStateChange
from .types.error_info import ErrorInfo
from .types.events import ConnectionEvent


class ConnectionManager:
    def __init__(self):
        self.previousState = ConnectionState.INITIALIZED
        self.currentState = ConnectionState.INITIALIZED

    def stateChangeObject(self, state: ConnectionState, event: ConnectionEvent = None, reason: ErrorInfo = None) -> ConnectionStateChange:
        previousState = self.currentState
        self.currentState = state
        self.previousState = previousState

        state_change = {
            "current": state,
            "previous": self.previousState
        }

        if event is not None:
            state_change["event"] = event

        if reason is not None:
            state_change["reason"] = reason

        return ConnectionStateChange(**state_change)
