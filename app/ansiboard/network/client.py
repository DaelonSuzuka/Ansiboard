from qtstrap import *
from qtpy.QtNetwork import *
from qtpy.QtWebSockets import *

import logging

class Client(QObject):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.log = logging.getLogger(__name__)
  
        self.connect_on_startup = QSettings().value('connect_on_startup', False) == 'true'
        self.current_connection = QSettings().value('current_connection', '10.0.0.207')
        default_previous_connections = ['ldg.hopto.org', 'daelon.hopto.org', '10.0.0.207']
        self.previous_connections = QSettings().value('previous_connections', default_previous_connections)
        
        self.socket = QWebSocket()
        self.socket.connected.connect(lambda: self.log.info("Connected to server"))
        self.socket.textMessageReceived.connect(self.process_message)

    def connect_to_remote(self, address=None):
        if address is not None:
            self.current_connection = address
            QSettings().setValue('current_connection', self.current_connection)
            if address not in self.previous_connections:
                self.previous_connections.append(address)

        self.open_socket()
        
    def open_socket(self):
        url = f'ws://{self.current_connection}:43000/control'
        self.log.info(f"Attempting to connect to server at: {QUrl(url)}")
        self.socket.open(QUrl(url))
        
    def close_socket(self):
        self.log.info(f"Closing socket")
        self.socket.close()
        
    def send_message(self, message):
        self.log.debug(f"TX: {message}")
        self.socket.sendTextMessage(message)
        
    def process_message(self, message):
        self.log.debug(f"RX: {message}")

        try:
            msg = json.loads(message)
        except:
            return