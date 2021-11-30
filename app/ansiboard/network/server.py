from qtstrap import *
from qtpy.QtNetwork import *
from qtpy.QtWebSockets import *
from urllib.parse import urlparse

import logging

class Server(QObject):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.log = logging.getLogger(__name__)

        self.server = QWebSocketServer('server-name', QWebSocketServer.NonSecureMode)
        self.client = None
        self.sockets = {}
        
        if self.server.listen(address=QHostAddress.Any, port=43000):
            self.log.info(f"Device server listening at: {self.server.serverAddress().toString()}:{str(self.server.serverPort())}")
        else:
            self.log.info('Failed to start device server.')

        self.server.newConnection.connect(self.on_new_connection)
        self.server.newConnection.connect(lambda: self.log.info(f'socket connected'))
    
    def on_new_connection(self):
        socket = self.server.nextPendingConnection()
        socket.disconnected.connect(lambda: self.log.info("socket disconnected"))
        url = urlparse(socket.resourceName())

        self.client = socket
        self.client.textMessageReceived.connect(self.processTextMessage)
        self.client.disconnected.connect(lambda: self.client.deleteLater())

    def processTextMessage(self, message):
        self.log.debug(f"RX: {message}")
        
        try: 
            msg = json.loads(message)
        except:
            return

    def send_later(self, message):
        QTimer.singleShot(10, lambda: self.client.sendTextMessage(message))