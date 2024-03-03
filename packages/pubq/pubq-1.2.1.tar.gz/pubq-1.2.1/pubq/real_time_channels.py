from .app import App
from .defaults.default_channel_events import DefaultChannelEvents
from .types.events import ChannelEvent
from .types.listeners import ChannelListener, MessageListener
from .types.states import ChannelState
from .websocket import WebSocket
from .channel_manager import ChannelManager
from .message import Message
from .types.common_options import CommonOptions
from .types.message import MessageObject
from pyee.base import EventEmitter


class RealTimeChannels:
    def __init__(self, options: CommonOptions):
        self.options = options
        self.__ws = WebSocket.getInstance()
        self.__app = App.getInstance()
        self.__channel = None
        self.__events = EventEmitter()
        self.__manager = ChannelManager()

    @property
    def state(self) -> ChannelState:
        return self.__manager.currentState

    def get(self, channelName: str):
        self.__channel = f"{self.__app.getId()}/{channelName}"
        return self

    def __handle_subscribe_event(self, scc_channel, error, object):
        if error == '':
            self.__events.emit(
                "subscribed", self.__manager.stateChangeObject(ChannelState.SUBSCRIBED))
        else:
            self.__handle_subscribe_fail_event(error)

    def __handle_unsubscribe_event(self, scc_channel, error, object):
        if error == '':
            self.__events.emit(
                "unsubscribed", self.__manager.stateChangeObject(ChannelState.UNSUBSCRIBED))
        else:
            self.__handle_subscribe_fail_event(error)

    def __handle_subscribe_fail_event(self, error):
        self.__events.emit("failed", self.__manager.stateChangeObject(
            ChannelState.FAILED, "failed", error))

    def __handle_channel_data_event(self, listener: MessageListener):
        socket = self.__ws.getSocket()

        def __channel_message_handler(scc_channel, data):
            msg_obj = MessageObject(data=data)
            msg = Message(msg_obj).toObject()
            listener(msg)

        socket.onchannel(self.__channel, __channel_message_handler)

    def subscribe(self, arg1, arg2=None):
        socket = self.__ws.getSocket()

        if not self.__channel:
            raise ValueError("Channel is not specified.")
        self.__events.emit(
            "subscribing", self.__manager.stateChangeObject(ChannelState.SUBSCRIBING))
        if isinstance(arg1, str) and callable(arg2):
            # Overload 1
            pass
        elif isinstance(arg1, list) and callable(arg2):
            # Overload 2
            pass
        elif callable(arg1) and arg2 is None:
            # Overload 3
            socket.subscribeack(self.__channel, self.__handle_subscribe_event)
            self.__handle_channel_data_event(arg1)

    def unsubscribe(self, arg1=None, arg2=None):
        socket = self.__ws.getSocket()

        if not self.__channel:
            raise ValueError("Channel is not specified.")
        self.__events.emit(
            "unsubscribing", self.__manager.stateChangeObject(ChannelState.UNSUBSCRIBING))
        if isinstance(arg1, str) and callable(arg2):
            # Overload 1
            pass
        elif isinstance(arg1, list) and callable(arg2):
            # Overload 2
            pass
        elif isinstance(arg1, str) and arg2 is None:
            # Overload 3
            pass
        elif isinstance(arg1, list) and arg2 is None:
            # Overload 4
            pass
        elif callable(arg1) and arg2 is None:
            # Overload 5
            pass
        elif arg1 is None and arg2 is None:
            socket.unsubscribeack(
                self.__channel, self.__handle_unsubscribe_event)  # Overload 6

    def on(self, arg1, arg2=None):
        if arg1 is not None and callable(arg2):
            # Overload 1
            self.__events.on(arg1, arg2)
        elif isinstance(arg1, list) and callable(arg2):
            # Overload 2
            for event_name in arg1:
                self.__events.on(event_name, arg2)
        elif callable(arg1) and arg2 is None:
            # Overload 3
            for event_name in DefaultChannelEvents:
                self.__events.on(event_name, arg1)
        else:
            raise ValueError("Invalid arguments")

    def once(self, arg1, arg2=None):
        if isinstance(arg1, ChannelEvent) and callable(arg2):
            # Overload 1
            self.__events.once(arg1, arg2)
        elif callable(arg1) and arg2 is None:
            # Overload 2
            for event_name in DefaultChannelEvents:
                self.__events.once(event_name, arg1)
        else:
            raise ValueError("Invalid arguments")

    def off(self, arg1=None, arg2=None):
        if isinstance(arg1, ChannelEvent) and callable(arg2):
            # Overload 1
            self.__events.remove_listener(arg1, arg2)
        elif isinstance(arg1, list) and callable(arg2):
            # Overload 2
            for event_name in arg1:
                self.__events.remove_listener(event_name, arg2)
        elif isinstance(arg1, ChannelEvent):
            # Overload 3
            self.__events.remove_listener(arg1)
        elif isinstance(arg1, list):
            # Overload 4
            self.__events.remove_all_listeners(arg1)
        elif callable(arg1):
            # Overload 5
            self.__events.remove_listener(arg1)
        elif arg1 is None and arg2 is None:
            # Overload 6
            self.__events.remove_all_listeners()
        else:
            raise ValueError("Invalid arguments")

    def destroy(self):
        if (self.__channel):
            self.__channel.unsubscribe()
        self.off()
