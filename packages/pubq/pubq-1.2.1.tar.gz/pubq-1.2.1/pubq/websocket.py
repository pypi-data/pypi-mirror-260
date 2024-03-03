from socketclusterclient import Socketcluster


class WebSocket:
    __instance = None

    def __init__(self, scc_options):
        self.__scc_options = scc_options
        self.socket = None

    @classmethod
    def getInstance(cls, scc_options=None):
        if not cls.__instance and scc_options:
            cls.__instance = cls(scc_options)
        return cls.__instance

    def getSocket(self):
        return self.socket

    async def setSocket(self, handle_connect_event, handle_close_event, handle_error_event, handle_authenticate_event, handle_authentication_event):
        schema = "wss://" if self.__scc_options["secure"] else "ws://"
        port = f":" + \
            self.__scc_options["port"] if not self.__scc_options["secure"] else ''
        self.socket = Socketcluster.socket(
            schema + self.__scc_options["hostname"] + port + self.__scc_options["path"])

        self.socket.setBasicListener(
            handle_connect_event, handle_close_event, handle_error_event)

        self.socket.setAuthenticationListener(
            handle_authenticate_event, handle_authentication_event)
