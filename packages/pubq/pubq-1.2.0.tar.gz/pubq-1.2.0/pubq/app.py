from .auth import Auth
from .types.common_options import CommonOptions
from .utils.jwt import getJwtPayload, getSignedAuthToken


class App:
    __instance = None

    def __init__(self):
        self.id = None

    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            cls.__instance = cls()
        return cls.__instance

    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id

    def extractAndSetId(self, public_key):
        app_id = public_key.split(".")[0]
        self.setId(app_id)
        return self.id

    def handleAppId(self, options: CommonOptions, auth: Auth):
        if self.getId() is None:
            auth_method = auth.getAuthMethod()

            if auth_method == "Bearer":
                token = getSignedAuthToken(options.authTokenName)
                payload = getJwtPayload(token)
                if payload:
                    self.extractAndSetId(payload.get("sub"))
            elif auth_method == "Basic" and options.get("key") is not None:
                self.extractAndSetId(options.get("key"))

    def destroy(self):
        self.id = None
