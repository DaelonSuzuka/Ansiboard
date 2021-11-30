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
        self.server =  QApplication.instance().server
        self.server.message_received.connect(self.event_recieved)

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
        event.accept()
        print(type(event))
        # if event.type() == QEvent.TabletPress:
        # elif event.type() == QEvent.TabletRelease:
        # elif event.type() == QEvent.TabletMove:
        d = {
            'posF': str(event.posF()),
            'xTilt': str(event.xTilt()),
            'yTilt': str(event.yTilt()),
            'pressure': str(event.pressure()),
            'pointerType': str(event.pointerType()),
        }
        self.event_recieved(d)
        self.client.send_message(json.dumps(d))

    def event_recieved(self, msg):
        try:
            self.pos.setText(str(msg['posF']))
            self.xtilt.setText(str(msg['xTilt']))
            self.ytilt.setText(str(msg['yTilt']))
            self.pressure.setText(str(msg['pressure']))
            self.pointer.setText(str(msg['pointerType']))
        except:
            pass

    # def eventFilter(self, obj, event):
    #     if event.type() == QEvent.TouchBegin:  # Catch the TouchBegin event.
    #         print('We have a touch begin')
    #         return True
    #     elif event.type() == QEvent.TouchEnd:  # Catch the TouchEnd event.
    #         print('We have a touch end')
    #         return True
    #     elif event.type() == QEvent.TouchUpdate:  # Catch the TouchEnd event.
    #         print('We have a touch update')
    #         return True
    #     elif event.type() == QEvent.MouseButtonPress:
    #         d = {
    #             'event': 'click',
    #         }

    #         self.client.send_message(json.dumps(d))
    #         return True
    #     elif event.type() == QEvent.MouseMove:
    #         print('mouse move')
    #         return True

    #     return super().eventFilter(obj, event)