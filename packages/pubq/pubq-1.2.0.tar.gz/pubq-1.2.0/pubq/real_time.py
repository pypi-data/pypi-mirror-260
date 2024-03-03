from typing import Optional
from .app import App
from .types.common_options import CommonOptions
from .defaults.default_common_options import DefaultCommonOptions
from .defaults.default_private_options import DefaultPrivateOptions
from .auth import Auth
from .connection import Connection
from .real_time_channels import RealTimeChannels


class RealTime:
    def __init__(self, options: Optional[CommonOptions] = None):

        merged_options = {
            **DefaultCommonOptions,
            **(options if options else {}),
            **DefaultPrivateOptions
        }

        self.options = merged_options

        self.connection = Connection(self.options)
        self.channels = RealTimeChannels(self.options)
        self.auth = Auth.getInstance()
        self.app = App.getInstance()

    def destroy(self):
        self.auth.destroy()
        self.connection.destroy()
        self.channels.destroy()
        self.app.destroy()
