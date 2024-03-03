from typing import Optional

from .types.error_info import ErrorInfo
from .types.events import ChannelEvent
from .types.states import ChannelState
from .types.channel import ChannelStateChange


class ChannelManager:
    def __init__(self):
        self.previousState: Optional[ChannelState] = ChannelState.INITIALIZED
        self.currentState: Optional[ChannelState] = ChannelState.INITIALIZED

    def stateChangeObject(self, state: ChannelState, event: Optional[ChannelEvent] = None,
                            reason: Optional[ErrorInfo] = None) -> ChannelStateChange:
        previousState = self.currentState
        self.currentState = state

        return ChannelStateChange(
            current=state,
            previous=previousState,
            event=event,
            reason=reason
        )
