from __future__ import print_function

from OpenGL.GL import *
from OpenGL.GL import shaders
import sys

def file_read(filename):
    file = open(filename)
    res = file.read()
    file.close()

    return res


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def print_log(object: GLuint):
    log_length = GLuint
    log = ''

    if glIsShader(object):
        glGetShaderiv(object, GL_INFO_LOG_LENGTH, log_length)
        glGetShaderInfoLog(object, log_length, None, log)
    elif glIsProgram:
        glGetProgramiv(object, GL_INFO_LOG_LENGTH, log_length)
        glGetProgramInfoLog(object, log_length, None, log)
    else:
        eprint("printlog: Not a shader or a program")
        return

    eprint(log)


def create_program(vertexfile, fragmentfile):
    vertexShader = file_read(vertexfile)
    fragmentShader = file_read(fragmentfile)
    vs = shaders.compileShader(vertexShader, GL_VERTEX_SHADER)
    fs = shaders.compileShader(fragmentShader, GL_FRAGMENT_SHADER)
    program = shaders.compileProgram(vs, fs)

    return program


def get_attrib(program, name):
    attribute = glGetAttribLocation(program, name)
    if attribute == -1:
        eprint("Could not bind attribute ", name)
    return attribute


def get_uniform(program, name):
    uniform = glGetUniformLocation(program, name)
    if uniform == -1:
        eprint("Could not bind uniform ", name)
    return uniform
