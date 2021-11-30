from qtstrap import *
import qtawesome as qta
from ansiboard.network import NetworkStatusWidget
import json


class Stroke:
    def __init__(self):
        self.points = []

    def add_point(self, point):
        self.points.append(point)


class Canvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        self.client = QApplication.instance().client
        self.server =  QApplication.instance().server
        self.server.message_received.connect(self.receive_data)

        self.strokes = []
        self.stroke = None

    def add_stroke(self, stroke):
        self.strokes.append(stroke)
    
    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        for s in self.strokes:
            p.drawPath(s)

        if self.stroke:
            p.drawPath(self.stroke)
        p.end()

    def tabletEvent(self, event):
        data = {}
        event.accept()
        if event.type() == QEvent.TabletPress:
            data['event'] = 'press'
            data['type'] = event.pointerType()
        elif event.type() == QEvent.TabletMove:
            data['event'] = 'move'
        elif event.type() == QEvent.TabletRelease:
            data['event'] = 'release'

        data['pos'] = event.posF()
        self.receive_data(data)
        self.client.send_message(json.dumps(data))

    def receive_data(self, data):
        if data['event'] == 'press':
            if data['type'] == QTabletEvent.PointerType.Pen:
                self.stroke = QPainterPath()
                self.stroke.moveTo(data['pos'])
                self.update()
        if data['event'] == 'move':
            if self.stroke:
                self.stroke.lineTo(data['pos'])
                self.update()
        if data['event'] == 'release':
            if self.stroke:
                self.add_stroke(self.stroke)
                self.stroke = None
                self.update()


class MainWindow(BaseMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setAttribute(Qt.WA_AcceptTouchEvents, True)
        self.installEventFilter(self)
        self.network_status = NetworkStatusWidget(self)

        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)

        self.init_statusbar()
        
    def init_statusbar(self):
        self.status = BaseToolbar(self, 'statusbar', location='bottom', size=30)
        self.status.setContextMenuPolicy(Qt.PreventContextMenu)
        
        self.status.add_spacer()
        self.status.addWidget(self.network_status)

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