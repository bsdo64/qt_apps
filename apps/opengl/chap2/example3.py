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


def open_file(file_url):
    f = open(file_url, 'r')
    data = f.read()
    f.close()
    print(data)
    return data


def compile_shaders():
    vertex_shader_source = open_file('graph.v.glsl')
    fragment_shader_source = open_file('graph.f.glsl')

    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex_shader, vertex_shader_source)
    glCompileShader(vertex_shader)

    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader, fragment_shader_source)
    glCompileShader(fragment_shader)

    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return program


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

        self.rendering_program = compile_shaders()
        self.vertex_array_object = glGenVertexArrays(1)

        glBindVertexArray(self.vertex_array_object)

    def paintGL(self):
        """Painting callback that uses the initialized OpenGL functions."""
        now = time.time() * 5
        color = np.array([
            np.sin(now),
            np.cos(now),
            0., 1.
        ], dtype=np.float32)

        glClearBufferfv(GL_COLOR, 0, color)

        glUseProgram(self.rendering_program)

        glDrawArrays(GL_POINTS, 0, 1)
        glPointSize(40.0)

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