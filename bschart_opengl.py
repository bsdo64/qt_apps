from PyQt5.QtCore import QTimer
from PyQt5.QtGui import (
        QOpenGLBuffer,
        QOpenGLShader,
        QOpenGLShaderProgram,
        QOpenGLVersionProfile,
        QOpenGLVertexArrayObject,
        QSurfaceFormat,
    )
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
import numpy as np
import time

from OpenGL.GL import *


class QOpenGLControllerWidget(QOpenGLWidget):
    """Widget that sets up specific OpenGL version profile."""

    def __init__(self, versionprofile=None, *args, **kwargs):
        """Initialize OpenGL version profile."""
        super(QOpenGLControllerWidget, self).__init__(*args, **kwargs)

        self.versionprofile = versionprofile

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_color)
        self.timer.start(10)

    def update_color(self):
        self.update()

    def initializeGL(self):
        """Apply OpenGL version profile and initialize OpenGL functions."""

        print('Opengl Version : ', glGetString(GL_VERSION))

        self.createShaders()
        self.createVBO()
        glClearColor(0.0, 0.0, 0.0, 0.0)

    def paintGL(self):
        """Painting callback that uses the initialized OpenGL functions."""
        red = np.array([
            np.sin(time.time()) * 0.5 + 0.5,
            np.cos(time.time()) * 0.5 + 0.5,
            0., 1], dtype=np.float32)

        glClearBufferfv(GL_COLOR, 0, red)

        # self.gl.glClear(self.gl.GL_COLOR_BUFFER_BIT | self.gl.GL_DEPTH_BUFFER_BIT)
        # self.gl.glDrawArrays(self.gl.GL_TRIANGLES, 0, 3)

    def resizeGL(self, w, h):
        """Resize viewport to match widget dimensions."""
        glViewport(0, 0, w, h)

    def createShaders(self):
        ...

    def createVBO(self):
        ...


class QTWithGLTest(QMainWindow):
    """Main window."""

    def __init__(self, versionprofile=None, *args, **kwargs):
        """Initialize with an OpenGL Widget."""
        super(QTWithGLTest, self).__init__(*args, **kwargs)

        self.widget = QOpenGLControllerWidget(versionprofile=versionprofile)
        self.setCentralWidget(self.widget)
        self.show()


if __name__ == '__main__':
    import sys

    fmt = QSurfaceFormat()
    fmt.setVersion(4, 1)
    fmt.setProfile(QSurfaceFormat.CoreProfile)
    fmt.setSamples(4)
    QSurfaceFormat.setDefaultFormat(fmt)

    vp = QOpenGLVersionProfile()
    vp.setVersion(4, 1)
    vp.setProfile(QSurfaceFormat.CoreProfile)

    app = QApplication(sys.argv)
    window = QTWithGLTest(versionprofile=vp)
    window.show()
    sys.exit(app.exec_())