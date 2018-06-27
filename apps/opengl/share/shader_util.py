from OpenGL.GL import *


def open_file(file_url):
    f = open(file_url, 'r')
    data = f.read()
    f.close()
    return data


def compile_shaders(vertex_file, fragment_file):
    vertex_shader_source = open_file(vertex_file)
    fragment_shader_source = open_file(fragment_file)

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
