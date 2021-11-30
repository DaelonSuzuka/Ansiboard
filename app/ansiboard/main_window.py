from qtstrap import *
import qtawesome as qta
from ansiboard.network import NetworkStatusWidget
import json

class MainWindow(BaseMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setAttribute(Qt.WA_AcceptTouchEvents, True)
        self.installEventFilter(self)
        self.network_status = NetworkStatusWidget(self)

        self.client = QApplication.instance().client
        QApplication.instance().server.cb = self.event_recieved

        self.pos = QLabel()
        self.xtilt = QLabel()
        self.ytilt = QLabel()
        self.pressure = QLabel()
        self.pointer = QLabel()
        self.debug = QLabel()

        with CVBoxLayout(self) as layout:
            layout.add(self.pos)
            with layout.hbox():
                layout.add(self.xtilt)
                layout.add(self.ytilt)
                layout.add(QLabel(), 1)
            layout.add(self.pressure)
            layout.add(self.pointer)
            layout.add(self.debug)
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

        d = {
            'posF': str(event.posF()),
            'xTilt': str(event.xTilt()),
            'yTilt': str(event.yTilt()),
            'pressure': str(event.pressure()),
            'pointerType': str(event.pointerType()),
        }
        s = json.dumps(d)
        self.debug.setText(s)
        self.client.send_message(s)

    def event_recieved(msg):
        self.pos.setText(str(msg['posF']))
        self.xtilt.setText(str(msg['xTilt']))
        self.ytilt.setText(str(msg['yTilt']))
        self.pressure.setText(str(msg['pressure']))
        self.pointer.setText(str(msg['pointerType']))

    def eventFilter(self, obj, event):
        if event.type() == QEvent.TouchBegin:  # Catch the TouchBegin event.
            print('We have a touch begin')
            return True
        elif event.type() == QEvent.TouchEnd:  # Catch the TouchEnd event.
            print('We have a touch end')
            return True

        return super().eventFilter(obj, event)