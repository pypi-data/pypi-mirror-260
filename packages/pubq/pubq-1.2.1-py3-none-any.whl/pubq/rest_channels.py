from .auth import Auth
from .http import Http
from .types.listeners import ErrorListener
from typing import Union, List, Any


class RESTChannels:
    def __init__(self, auth: Auth):
        self.__http = Http()
        self.__client = self.__http.getClient()
        self.__version = "v1"
        self.__auth = auth
        self.__channel = None

    def get(self, channelName: str):
        self.__channel = channelName
        return self

    def publish(
        self,
        arg1: Union[str, List[str], Any, List[Any]],
        arg2: Union[Any, List[Any], ErrorListener] = None,
        arg3: ErrorListener = None
    ):
        if isinstance(arg1, str) and callable(arg3):
            # Overload 1
            pass
        elif isinstance(arg1, list) and arg2 is not None and callable(arg3):
            # Overload 2
            pass
        elif isinstance(arg1, list) and callable(arg2):
            # Overload 3
            pass
        elif isinstance(arg1, list) and arg2 is None:
            # Overload 6
            pass
        elif arg2 is None:
            # Overload 5
            self.__client.post(
                f"/{self.__version}/channels/{self.__channel}/messages",
                json={
                    "data": arg1,
                },
                headers={
                    "Authorization": self.__auth.makeAuthorizationHeader(),
                }
            )
        else:
            # Overload 4
            pass
