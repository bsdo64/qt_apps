from PyQt5.QtCore import QPointF, Qt, QRectF, QRect, QTimer
from PyQt5.QtGui import QColor, QSurfaceFormat, QLinearGradient, QBrush, QPen, QFont, QPaintEvent, QPainter
from PyQt5.QtWidgets import QApplication, QOpenGLWidget, QWidget, QLabel, QGridLayout

import pyqtgraph

class Helper(object):
    def __init__(self):
        gradient = QLinearGradient(QPointF(50, -20), QPointF(80, 20))
        gradient.setColorAt(0.0, Qt.white)
        gradient.setColorAt(1.0, QColor(0xa6, 0xce, 0x39))

        self.background = QBrush(QColor(64,32,64))
        self.circleBrush = QBrush(gradient)
        self.circlePen = QPen(Qt.black)
        self.textPen = QPen(Qt.black)
        self.textFont = QFont()

        self.textFont.setPixelSize(50)

    def paint(self, painter, event, elapsed):
        painter.fillRect(event.rect(), self.background)
        painter.translate(100, 100)

        painter.save()
        painter.setBrush(self.circleBrush)
        painter.setPen(self.circlePen)
        painter.rotate(elapsed * 0.030)

        r = elapsed / 1000.0
        n = 30
        for i in range(n):
            painter.rotate(30)
            factor = (i + r) / n
            radius = 0 + 120.0 * factor
            circleRadius = 1 + factor * 20
            painter.drawEllipse(QRectF(radius, -circleRadius,
                                       circleRadius * 2, circleRadius * 2))
        painter.restore()

        painter.setPen(self.textPen)
        painter.setFont(self.textFont)
        painter.drawText(QRect(-50, -50, 100, 100), Qt.AlignCenter, "Qt")


class GLWidget(QOpenGLWidget):
    def __init__(self, helper: Helper, parent=None):
        QWidget.__init__(self, parent)
        self.helper = helper
        self.elapsed = 0
        self.setFixedSize(200, 200)
        self.setAutoFillBackground(False)

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.helper.paint(painter, event, self.elapsed)
        painter.end()

    def animate(self):
        self.elapsed = (self.elapsed + self.sender().interval()) % 1000
        self.update()


class Widget(QWidget):
    def __init__(self, helper: Helper, parent=None):
        QWidget.__init__(self, parent)
        self.helper = helper
        self.elapsed = 0
        self.setFixedSize(200, 200)

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.helper.paint(painter, event, self.elapsed)
        painter.end()

    def animate(self):
        self.elapsed = (self.elapsed + self.sender().interval()) % 1000
        self.update()


class Window(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.helper = Helper()
        
        self.setWindowTitle("2D Painting on Native and OpenGL Widgtes")

        native = Widget(self.helper, self)
        openGL = GLWidget(self.helper, self)

        openglLabel = QLabel('opengl')
        openglLabel.setAlignment(Qt.AlignCenter)

        nativeLabel = QLabel('Native')
        nativeLabel.setAlignment(Qt.AlignCenter)

        layout = QGridLayout()
        layout.addWidget(native, 0, 0)
        layout.addWidget(openGL, 0, 1)
        layout.addWidget(nativeLabel, 1, 0)
        layout.addWidget(openglLabel, 1, 1)
        self.setLayout(layout)

        timer = QTimer(self)
        timer.timeout.connect(native.animate)
        timer.timeout.connect(openGL.animate)

        timer.start(10)

        
if __name__ == '__main__':
    app = QApplication([])

    fmt = QSurfaceFormat()
    fmt.setSamples(4)
    QSurfaceFormat.setDefaultFormat(fmt)

    window = Window()
    window.show()

    app.exec()