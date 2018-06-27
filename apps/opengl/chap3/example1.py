from OpenGL.GL import *
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import (
        QOpenGLVersionProfile,
        QSurfaceFormat,
    )
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
import numpy as np
import time

from share import shader_util as shaders


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

        self.rendering_program = shaders.compile_shaders()
        self.vertex_array_object = glGenVertexArrays(1)

        glBindVertexArray(self.vertex_array_object)

    def paintGL(self):
        """Painting callback that uses the initialized OpenGL functions."""
        now = time.time() * 5
        color = np.array([
            np.sin(now) * 0.5 + 0.5,
            np.cos(now) * 0.5 + 0.5,
            0., 1.
        ], dtype=np.float32)
        glClearBufferfv(GL_COLOR, 0, color)

        glUseProgram(self.rendering_program)

        attrib = np.array([
            np.sin(now) * 0.5,
            np.cos(now) * 0.6,
            0., 0.
        ], dtype=np.float32)

        glVertexAttrib4fv(0, attrib)

        glDrawArrays(GL_TRIANGLES, 0, 3)

    def resizeGL(self, w, h):
        """Resize viewport to match widget dimensions."""
        glViewport(0, 0, w, h)


class OpenGLApp(QMainWindow):
    """Main window."""

    def __init__(self, versionprofile=None, *args, **kwargs):
        """Initialize with an OpenGL Widget."""
        super(OpenGLApp, self).__init__(*args, **kwargs)

        self.widget = QOpenGLControllerWidget(versionprofile=versionprofile)
        self.setMinimumSize(400, 400)
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
    window = OpenGLApp(versionprofile=vp)
    window.show()
    sys.exit(app.exec_())