from typing import Optional, Any, Dict
from .types.common_options import CommonOptions
from .defaults.default_common_options import DefaultCommonOptions
from .http import Http
from .auth import Auth
from .types.token_options import TokenOptions
from .rest_channels import RESTChannels


class REST:
    def __init__(self, options: Optional[CommonOptions] = None, auth: Optional[Auth] = None):
        merged_options = {
            **DefaultCommonOptions,
            **(options if options else {}),
        }

        self.options = merged_options

        self.__http = Http()
        self.__client = self.__http.getClient()
        self.__version = "v1"
        self.auth = auth if auth is not None else Auth.getInstance(
            self.options)
        self.channels = RESTChannels(self.auth)
        if self.options.get('autoRefreshToken'):
            self.auth.startRefreshTokenInterval()

    async def generateToken(self, options: Optional[TokenOptions] = None) -> Dict[str, Any]:
        response = await self.__client.post(
            f"/{self.__version}/keys/tokens",
            json={'clientId': options.clientId if options else None},
            headers={'Authorization': self.auth.makeAuthorizationHeader()}
        )
        return response

    async def refreshToken(self, token: str) -> Dict[str, Any]:
        response = await self.__client.post(
            f"/{self.__version}/keys/tokens/refresh",
            json={},
            headers={'Authorization': f'Bearer {token}'}
        )
        return response

    async def revokeToken(self, token: str) -> Dict[str, Any]:
        response = await self.__client.post(
            f"/{self.__version}/keys/tokens/revoke",
            json={},
            headers={'Authorization': f'Bearer {token}'}
        )
        return response
