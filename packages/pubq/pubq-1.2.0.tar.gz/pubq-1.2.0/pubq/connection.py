import asyncio
from .app import App
from .defaults.default_connection_events import DefaultConnectionEvents
from .types.common_options import CommonOptions
from .types.events import ConnectionEvent
from .types.listeners import ConnectionListener
from .types.states import ConnectionState
from .websocket import WebSocket
from .connection_manager import ConnectionManager
from .auth import Auth
from pyee.base import EventEmitter


class Connection:
    def __init__(self, options: CommonOptions):
        self.__options = options
        self.__ws = WebSocket.getInstance(self.__options)
        self.__app = App.getInstance()
        self.__auth = Auth.getInstance(self.__options)
        self.__events = EventEmitter()
        self.__manager = ConnectionManager()

        self.__app.handleAppId(self.__options, self.__auth)

        asyncio.create_task(self.__create_socket())

        asyncio.create_task(self.__auto_connect())

    @property
    def state(self):
        return self.__manager.currentState

    @property
    def id(self):
        socket = self.__ws.getSocket()
        return socket.id

    async def __create_socket(self):
        await self.__ws.setSocket(self.__handle_connect_event,
                                  self.__handle_close_event, self.__handle_error_event, self.__handle_authenticate_event, self.__handle_authentication_event)

    async def __auto_connect(self):
        if self.__options.get('autoConnect'):
            self.connect()

    def connect(self):
        socket = self.__ws.getSocket()
        if socket:
            self.__handle_connecting_event()
            socket.connect()

    def __handle_connecting_event(self):
        self.__events.emit('connecting', self.__manager.stateChangeObject(
            ConnectionState.CONNECTING))

    def __handle_connect_event(self):
        pass

    # This event occurs only when the socket is authenticated using basic auth
    def __handle_authenticate_event(self, scc_socket, scc_auth_token):
        socket = self.__ws.getSocket()
        socket.setAuthtoken(scc_auth_token)
        self.__events.emit(
            'connected', self.__manager.stateChangeObject(ConnectionState.CONNECTED))

    def __handle_authentication_event(self, scc_socket, is_authenticated):
        if is_authenticated:
            self.__events.emit(
                'connected', self.__manager.stateChangeObject(ConnectionState.CONNECTED))
        elif not is_authenticated and self.__options.get('autoAuthenticate'):
            self.__auth.authenticate()

    def __handle_close_event(self):
        self.__events.emit(
            'closed', self.__manager.stateChangeObject(ConnectionState.CLOSED))

    def __handle_error_event(self, scc_socket, error):
        self.__events.emit('failed', self.__manager.stateChangeObject(
            ConnectionState.FAILED, ConnectionEvent.FAILED, error))

    def close(self):
        socket = self.__ws.getSocket()
        self.__events.emit(
            'closing', self.__manager.stateChangeObject(ConnectionState.CLOSING))
        socket.disconnect()

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
            for event_name in DefaultConnectionEvents:
                self.__events.on(event_name, arg1)
        else:
            raise ValueError('Invalid "on" arguments')

    def once(self, arg1, arg2=None):
        if isinstance(arg1, str) and callable(arg2):
            # Overload 1
            self.__events.once(arg1, arg2)
        elif callable(arg1) and arg2 is None:
            # Overload 2
            for event_name in DefaultConnectionEvents:
                self.__events.once(event_name, arg1)
        else:
            raise ValueError('Invalid "once" arguments')

    def off(self, arg1=None, arg2=None):
        if arg1 is not None and callable(arg2):
            # Overload 1
            self.__events.remove_listener(arg1, arg2)
        elif isinstance(arg1, list) and callable(arg2):
            # Overload 2
            for event_name in arg1:
                self.__events.remove_listener(event_name, arg2)
        elif isinstance(arg1, ConnectionEvent) and arg2 is None:
            # Overload 3
            self.__events.remove_listener(arg1)
        elif isinstance(arg1, list) and arg2 is None:
            # Overload 4
            self.__events.remove_all_listeners(arg1)
        elif callable(arg1) and arg2 is None:
            # Overload 5
            self.__events.remove_listener(arg1)
        elif arg1 is None and arg2 is None:
            # Overload 6
            self.__events.remove_all_listeners()
        else:
            raise ValueError('Invalid "off" arguments')

    def destroy(self):
        socket = self.__ws.getSocket()

        socket.disconnect()
        socket.setAuthtoken('')
        self.off()
