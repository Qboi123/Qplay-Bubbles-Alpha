from pyglet.gl import *


def setup_gl():
    pass


def setup():
    # glClearColor(0.1, 0.5, 0.55, 1)
    glEnable(GL_ALPHA_TEST)
    glEnable(GL_SCISSOR_TEST)
    glEnable(GL_STENCIL_TEST)
    pass
