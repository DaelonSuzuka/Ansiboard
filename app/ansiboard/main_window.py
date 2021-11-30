from qtstrap import *
import qtawesome as qta
from ansiboard.network import NetworkStatusWidget


class MainWindow(BaseMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setAttribute(Qt.WA_AcceptTouchEvents, True)
        
        self.network_status = NetworkStatusWidget(self)

        self.pos = QLabel()
        self.xtilt = QLabel()
        self.ytilt = QLabel()
        self.pressure = QLabel()
        self.pointer = QLabel()

        with CVBoxLayout(self) as layout:
            layout.add(self.pos)
            with layout.hbox():
                layout.add(self.xtilt)
                layout.add(self.ytilt)
                layout.add(QLabel(), 1)
            layout.add(self.pressure)
            layout.add(self.pointer)
            layout.add(QLabel(), 1)

        self.init_statusbar()
        
    def init_statusbar(self):
        self.status = BaseToolbar(self, 'statusbar', location='bottom', size=30)
        self.status.setContextMenuPolicy(Qt.PreventContextMenu)
        
        self.status.add_spacer()
        

        self.status.addWidget(self.network_status)

    def tabletEvent(self, event):
        self.pos.setText(str(event.posF()))
        self.xtilt.setText(str(event.xTilt()))
        self.ytilt.setText(str(event.yTilt()))
        self.pressure.setText(str(event.pressure()))
        self.pointer.setText(str(event.pointerType()))

    def touchEvent(self, event):
        print(event)