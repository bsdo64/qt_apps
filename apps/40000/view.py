from PyQt5.QtCore import pyqtSlot, Qt, QSize, QRectF
from PyQt5.QtGui import QWheelEvent, QPainter, QPixmap, QIcon, QTransform, QSurfaceFormat
from PyQt5.QtOpenGL import QGLWidget, QGLFormat, QGL
from PyQt5.QtWidgets import QGraphicsView, QFrame, QStyle, QToolButton, QSlider, QVBoxLayout, QHBoxLayout, QLabel, \
    QButtonGroup, QGridLayout, QWidget, QOpenGLWidget


class GraphicsView(QGraphicsView):
    def __init__(self, v):
        super().__init__()

        self.view = v

    def wheelEvent(self, e: QWheelEvent):
        if e.modifiers() and Qt.ControlModifier:
            if e.angleDelta().y() > 0:
                self.view.zoomIn(6)
            else:
                self.view.zoomOut(6)

        else:
            super().wheelEvent(e)


class View(QFrame):
    def __init__(self, name, parent=None):
        super().__init__(parent)

        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.graphicsView = GraphicsView(self)
        self.graphicsView.setRenderHint(QPainter.Antialiasing, False)
        self.graphicsView.setDragMode(QGraphicsView.RubberBandDrag)
        self.graphicsView.setOptimizationFlags(QGraphicsView.DontSavePainterState)
        self.graphicsView.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        self.graphicsView.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        size = self.style().pixelMetric(QStyle.PM_ToolBarIconSize)
        iconSize = QSize(size, size)

        zoomInIcon = QToolButton()
        zoomInIcon.setAutoRepeat(True)
        zoomInIcon.setAutoRepeatInterval(33)
        zoomInIcon.setAutoRepeatDelay(0)
        zoomInIcon.setIcon(QIcon(QPixmap(':/images/zoomin.png')))
        zoomInIcon.setIconSize(iconSize)
        zoomOutIcon = QToolButton()
        zoomOutIcon.setAutoRepeat(True)
        zoomOutIcon.setAutoRepeatInterval(33)
        zoomOutIcon.setAutoRepeatDelay(0)
        zoomOutIcon.setIcon(QIcon(QPixmap(':/images/zoomout.png')))
        zoomOutIcon.setIconSize(iconSize)
        self.zoomSlider = QSlider()
        self.zoomSlider.setMinimum(0)
        self.zoomSlider.setMaximum(500)
        self.zoomSlider.setValue(250)
        self.zoomSlider.setTickPosition(QSlider.TicksRight)

        zoomSliderLayout = QVBoxLayout()
        zoomSliderLayout.addWidget(zoomInIcon)
        zoomSliderLayout.addWidget(self.zoomSlider)
        zoomSliderLayout.addWidget(zoomOutIcon)

        rotateLeftIcon = QToolButton()
        rotateLeftIcon.setIcon(QIcon(QPixmap(':/images/rotateleft.png')))
        rotateLeftIcon.setIconSize(iconSize)
        rotateRightIcon = QToolButton()
        rotateRightIcon.setIcon(QIcon(QPixmap(':/images/rotateright.png')))
        rotateRightIcon.setIconSize(iconSize)
        self.rotateSlider = QSlider()
        self.rotateSlider.setOrientation(Qt.Horizontal)
        self.rotateSlider.setMinimum(-360)
        self.rotateSlider.setMaximum(360)
        self.rotateSlider.setValue(0)
        self.rotateSlider.setTickPosition(QSlider.TicksBelow)

        rotateSliderLayout = QHBoxLayout()
        rotateSliderLayout.addWidget(rotateLeftIcon)
        rotateSliderLayout.addWidget(self.rotateSlider)
        rotateSliderLayout.addWidget(rotateRightIcon)

        self.resetButton = QToolButton()
        self.resetButton.setText('0')
        self.resetButton.setEnabled(False)

        labelLayout = QHBoxLayout()
        self.label = QLabel(name)
        self.label2 = QLabel("Pointer Mode")
        self.selectModeButton = QToolButton()
        self.selectModeButton.setText("Select")
        self.selectModeButton.setCheckable(True)
        self.selectModeButton.setChecked(True)
        self.dragModeButton = QToolButton()
        self.dragModeButton.setText("Drag")
        self.dragModeButton.setCheckable(True)
        self.dragModeButton.setChecked(False)
        self.openGlButton = QToolButton()
        self.openGlButton.setText("OpenGL")
        self.openGlButton.setCheckable(True)
        self.openGlButton.setEnabled(QGLFormat.hasOpenGL())
        self.antialiasButton = QToolButton()
        self.antialiasButton.setText("Antialiasing")
        self.antialiasButton.setCheckable(True)
        self.antialiasButton.setChecked(False)

        self.printButton = QToolButton()
        self.printButton.setIcon(QIcon(QPixmap(":/images/fileprint.png")))

        pointerModeGroup = QButtonGroup(self)
        pointerModeGroup.setExclusive(True)
        pointerModeGroup.addButton(self.selectModeButton)
        pointerModeGroup.addButton(self.dragModeButton)

        labelLayout.addWidget(self.label)
        labelLayout.addStretch()
        labelLayout.addWidget(self.label2)
        labelLayout.addWidget(self.selectModeButton)
        labelLayout.addWidget(self.dragModeButton)
        labelLayout.addStretch()
        labelLayout.addWidget(self.antialiasButton)
        labelLayout.addWidget(self.openGlButton)
        labelLayout.addWidget(self.printButton)

        topLayout = QGridLayout()
        topLayout.addLayout(labelLayout, 0, 0)
        topLayout.addWidget(self.graphicsView, 1, 0)
        topLayout.addLayout(zoomSliderLayout, 1, 1)
        topLayout.addLayout(rotateSliderLayout, 2, 0)
        topLayout.addWidget(self.resetButton, 2, 1)
        self.setLayout(topLayout)

        self.resetButton.clicked.connect(self.resetView)
        self.zoomSlider.valueChanged.connect(self.setupMatrix)
        self.rotateSlider.valueChanged.connect(self.setupMatrix)
        self.graphicsView.verticalScrollBar().valueChanged.connect(self.setResetButtonEnabled)
        self.graphicsView.horizontalScrollBar().valueChanged.connect(self.setResetButtonEnabled)
        self.selectModeButton.toggled.connect(self.togglePointerMode)
        self.dragModeButton.toggled.connect(self.togglePointerMode)
        self.antialiasButton.toggled.connect(self.toggleAntialiasing)
        self.openGlButton.toggled.connect(self.toggleOpenGL)
        rotateLeftIcon.clicked.connect(self.rotateLeft)
        rotateRightIcon.clicked.connect(self.rotateRight)
        zoomInIcon.clicked.connect(self.zoomIn)
        zoomOutIcon.clicked.connect(self.zoomOut)
        self.printButton.clicked.connect(self.print)

        self.setupMatrix()

    def view(self):
        return self.graphicsView

    def resetView(self):
        self.zoomSlider.setValue(250)
        self.rotateSlider.setValue(0)
        self.setupMatrix()
        self.graphicsView.ensureVisible(QRectF(0,0,0,0))

        self.resetButton.setEnabled(False)

    def setResetButtonEnabled(self):
        self.resetButton.setEnabled(True)

    def setupMatrix(self):
        scale = pow(2.0, (self.zoomSlider.value() - 250) / 50)
        matrix = QTransform()
        matrix.scale(scale, scale)
        matrix.rotate(self.rotateSlider.value())

        self.graphicsView.setTransform(matrix)
        self.setResetButtonEnabled()

    def togglePointerMode(self):

        self.graphicsView.setDragMode(
            QGraphicsView.RubberBandDrag if self.selectModeButton.isChecked() else QGraphicsView.ScrollHandDrag
        )
        self.graphicsView.setInteractive(self.selectModeButton.isChecked())

    def toggleOpenGL(self):
        vp = QWidget()

        if self.openGlButton.isChecked():
            fmt = QSurfaceFormat()
            fmt.setSamples(8)
            vp = QOpenGLWidget()
            vp.setFormat(fmt)

        self.graphicsView.setViewport(vp)


    def toggleAntialiasing(self):
        self.graphicsView.setRenderHint(QPainter.Antialiasing, self.antialiasButton.isChecked())

    def print(self):
        pass

    def zoomIn(self, level=1):
        self.zoomSlider.setValue(self.zoomSlider.value() + level)

    def zoomOut(self, level=1):
        self.zoomSlider.setValue(self.zoomSlider.value() - level)

    def rotateLeft(self):
        self.rotateSlider.setValue(self.rotateSlider.value() - 10)

    def rotateRight(self):
        self.rotateSlider.setValue(self.rotateSlider.value() + 10)
