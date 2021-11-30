from qtstrap import *
import qtawesome as qta

from ansiboard.network import DiscoveryService
from ansiboard.network import Client, Server


class Application(BaseApplication):
    def __init__(self) -> None:
        super().__init__()

        self.discovery = DiscoveryService(self)
        self.server = Server(self)
        self.client = Client(self)