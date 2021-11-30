from qtstrap import *
import qtawesome as qta


class NetworkStatusWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('NetworkStatusBarItem')

        self.hosts = []
        disc = QApplication.instance().discovery
        disc.host_found.connect(lambda h: self.hosts.append(h))
        disc.host_lost.connect(lambda h: self.hosts.remove(h))

        self.setAttribute(Qt.WA_AcceptTouchEvents, True)
    
        self.status = QLabel('Not Connected')
        self.icon_on = qta.icon('mdi.lan-connect', color='lightgray').pixmap(QSize(20, 20))
        self.icon_off = qta.icon('mdi.lan-disconnect', color='gray').pixmap(QSize(20, 20))
        self.icon = QLabel('')
        self.icon.setPixmap(self.icon_off)

        with CHBoxLayout(self, margins=(0, 0, 0, 0)) as layout:
            layout.add(self.icon)
            layout.add(self.status)
        
    def mousePressEvent(self, event):
        connect = QAction("Connect", self, triggered=self.connect_client)
        disconnect = QAction("Disconnect", self, triggered=self.disconnect_client)

        startup = QAction(
            "Connect at Startup", 
            self, 
            checkable=True, 
            # checked=bool(self.client.connect_on_startup),
            # triggered=self.client.toggle_connect_on_startup
        )

        menu = QMenu('', self)
        menu.addAction(connect)
        menu.addAction(disconnect)
        
        menu.addSeparator()
        for host in self.hosts:
            menu.addAction(QAction(host.hostname, self, triggered=lambda a=host.address: self.connect_client(a)))

        # menu.addSeparator()
        # for address in self.client.previous_connections:
        #     menu.addAction(QAction(address, self, triggered=lambda a=address: self.connect_client(a)))
        
        menu.addSeparator()
        menu.addAction(startup)

        menu.exec_(event.globalPos())

    def client_connected(self):
        # self.status.setText(self.client.current_connection)
        self.icon.setPixmap(self.icon_on)

    def client_disconnected(self):
        self.status.setText("Not Connected")
        self.icon.setPixmap(self.icon_off)

    def connect_client(self, address=None):
        self.status.setText("Connecting...")
        # self.client.disconnect_from_remote()
        # self.client.connect_to_remote(address)

    def disconnect_client(self):
        pass
        # self.client.disconnect_from_remote()
