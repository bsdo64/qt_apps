from ctypes import c_float, c_void_p

from OpenGL.GL import *
from PyQt5.QtCore import QTimer, QTime
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
        self.timer.setInterval(0)
        self.timer.start()
        self.timer.timeout.connect(self.update)

        self.frame_count = 0
        self.fps_timer = QTime()

    def initializeGL(self):
        """Apply OpenGL version profile and initialize OpenGL functions."""

        print('Opengl Version : ', glGetString(GL_VERSION))

        self.rendering_program = shaders.compile_shaders('graph.v.glsl', 'graph.f.glsl')
        self.vertex_array_object = glGenVertexArrays(1)

        glBindVertexArray(self.vertex_array_object)

    def paintGL(self):

        data = np.array([
            0.25, -0.25, 0.5, 1.0,
            -0.25, -0.25, 0.5, 1.0,
            0.25, 0.25, 0.5, 1.0,
        ])

        buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, buffer)
        glBufferData(GL_ARRAY_BUFFER, 1024 * 1024, None, GL_STATIC_DRAW)

        glBufferSubData(GL_ARRAY_BUFFER, 0, data.nbytes, data)

        ptr = glMapBuffer(GL_ARRAY_BUFFER, GL_WRITE_ONLY)
        c_void_p(ptr)

        self._update_fps()

        """Painting callback that uses the initialized OpenGL functions."""
        now = time.time() * 5
        color = np.array([
            np.sin(now) * 0.5 + 0.5,
            np.cos(now) * 0.5 + 0.5,
            0., 1.
        ], dtype=np.float32)
        glClearBufferfv(GL_COLOR, 0, color)

        glUseProgram(self.rendering_program)

        offset = np.array([
            np.sin(now) * 0.5,
            np.cos(now) * 0.6,
            0., 0.
        ], dtype=np.float32)

        color = np.array([
            np.cos(now) * 0.5 + 0.5,
            np.sin(now) * 0.5 + 0.5,
            0., 1.
        ], dtype=np.float32)

        glVertexAttrib4fv(0, offset)
        glVertexAttrib4fv(1, color)

        glDrawArrays(GL_LINE_LOOP, 0, 3)

    def resizeGL(self, w, h):
        """Resize viewport to match widget dimensions."""
        glViewport(0, 0, w, h)

    def _update_fps(self):
        if self.frame_count == 0:
            self.fps_timer.start()
        else:
            fps = self.frame_count / self.fps_timer.elapsed() * 1000
            self.parentWidget().setWindowTitle("FPS is {:.2f}".format(fps))
        self.frame_count += 1


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
    fmt.setSwapInterval(0)
    QSurfaceFormat.setDefaultFormat(fmt)

    vp = QOpenGLVersionProfile()
    vp.setVersion(4, 1)
    vp.setProfile(QSurfaceFormat.CoreProfile)

    app = QApplication(sys.argv)
    window = OpenGLApp(versionprofile=vp)
    window.show()
    sys.exit(app.exec_())