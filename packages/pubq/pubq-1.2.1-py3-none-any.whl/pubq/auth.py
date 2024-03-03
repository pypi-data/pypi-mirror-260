import threading
import base64
from .websocket import WebSocket
from .http import Http
from .utils.jwt import getJwtPayload, getSignedAuthToken
from .utils.time import getRemainingSeconds
from .utils.storage import storage


class Auth:
    __instance = None

    def __init__(self, options):
        self.__options = options
        self.__http = Http()
        self.__client = self.__http.getClient()
        self.__ws = WebSocket.getInstance()
        self.__refresh_token_interval_id = None

    @classmethod
    def getInstance(cls, options=None):
        if not cls.__instance and options:
            cls.__instance = cls(options)
        return cls.__instance

    def getAuthMethod(self):
        if self.__options.get("authUrl"):
            return "Bearer"
        elif self.__options.get("key"):
            return "Basic"
        return False

    def __get_key_or_token(self):
        if not self.__options.get("authTokenName"):
            raise ValueError("Auth token name cannot be empty.")

        if self.__options.get("authUrl"):
            return getSignedAuthToken(self.__options["authTokenName"])
        elif self.__options.get("key"):
            return self.getKeyBase64()
        return False

    def getKey(self):
        if self.__options.get("key"):
            return self.__options["key"]
        raise ValueError("API key has not been specified.")

    def getKeyBase64(self):
        return base64.b64encode(self.getKey().encode()).decode()

    def makeAuthorizationHeader(self):
        if self.getAuthMethod() and self.__get_key_or_token():
            return f"{self.getAuthMethod()} {self.__get_key_or_token()}"
        raise ValueError("Auth method has not been specified.")

    def basicAuth(self):
        socket = self.__ws.getSocket()
        socket.emitack("#basicAuth", {"key": self.getKey()}, self.__emit_ack)

    def __emit_ack(self, key, error, object):
        if error:
            raise error

    def authenticate(self, body=None, headers=None):
        auth_method = self.getAuthMethod()

        if auth_method == "Basic":
            self.basicAuth()
        # elif auth_method == "Bearer":
        #     token_data = await self.requestToken()
        #     self.__ws.getSocket().setAuthtoken(token_data["token"])

    def deauthenticate(self):
        self.requestRevoke()
        self.__ws.getSocket().setAuthtoken('')

    async def requestToken(self):
        if self.__options.get("authUrl"):
            try:
                response = await self.__client.post(
                    self.__options["authUrl"],
                    json=self.__options.get("authBody", {}),
                    headers=self.__options.get("authHeaders", {})
                )

                storage.set(
                    self.__options["authTokenName"],
                    response.data["data"]["token"]
                )

                return response.data["data"]
            except Exception as error:
                print(f"Error in request_token: {error}")
                raise error
        raise ValueError("Auth URL has not been provided.")

    async def requestRefresh(self):
        if self.__options.get("refreshUrl"):
            try:
                body = {
                    **self.__options.get("authBody", {}),
                    "token": self.__ws.socket.getAuthToken(),
                }

                response = await self.__client.post(
                    self.__options["refreshUrl"],
                    json=body,
                    headers=self.__options.get("authHeaders", {})
                )

                storage.set(
                    self.__options["authTokenName"],
                    response.data["data"]["token"]
                )

                self.__ws.getSocket().setAuthtoken(
                    response.data["data"]["token"])

                return response.data["data"]
            except Exception as error:
                print(f"Error in request_refresh: {error}")
                raise error
        raise ValueError("Refresh URL has not been provided.")

    async def requestRevoke(self):
        if self.__options.get("revokeUrl"):
            try:
                body = {
                    **self.__options.get("authBody", {}),
                    "token": self.__ws.socket.getAuthToken(),
                }

                response = await self.__client.post(
                    self.__options["revokeUrl"],
                    json=body,
                    headers=self.__options.get("authHeaders", {})
                )

                storage.remove(self.__options["authTokenName"])

                return response.data["data"]
            except Exception as error:
                print(f"Error in request_revoke: {error}")
                raise error
        raise ValueError("Revoke URL has not been provided.")

    def startRefreshTokenInterval(self):
        if self.getAuthMethod() == "Bearer":
            # Stop if any refresh token interval exists
            self.stopRefreshTokenInterval()

            self.__refresh_token_interval_id = threading.Timer(
                self.__options["refreshTokenInterval"],
                self.__refresh_token_interval_callback
            )
            self.__refresh_token_interval_id.start()

    def stopRefreshTokenInterval(self):
        if self.__refresh_token_interval_id:
            self.__refresh_token_interval_id.cancel()

    def __refresh_token_interval_callback(self):
        token = self.__ws.socket.getAuthToken()
        auth_token = getJwtPayload(token)

        if auth_token:
            remaining_seconds = getRemainingSeconds(auth_token["exp"])
            if remaining_seconds <= 60:
                self.requestRefresh()

    def destroy(self):
        self.stopRefreshTokenInterval()
