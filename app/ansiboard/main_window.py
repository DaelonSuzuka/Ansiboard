from qtstrap import *
import qtawesome as qta
from ansiboard.network import NetworkStatusWidget


class MainWindow(BaseMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # self.setCentralWidget()
        self.network_status = NetworkStatusWidget(self)

        self.init_statusbar()
        
    def init_statusbar(self):
        self.status = BaseToolbar(self, 'statusbar', location='bottom', size=30)
        self.status.setContextMenuPolicy(Qt.PreventContextMenu)
        
        self.status.add_spacer()
        

        self.status.addWidget(self.network_status)