import os

import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from object_loader.object_loader import ObjectLoader
from texture.texture_loader import load_texture
from camera.camera import Camera


mycam = Camera()
WIDTH, HEIGHT = 1280, 720
lastX, lastY = WIDTH / 2, HEIGHT / 2
first_mouse = True
left, right, forward, backward = False, False, False, False


# the keyboard input callback
def key_input_clb(window, key, scancode, action, mode):
    global left, right, forward, backward
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)
    if key == glfw.KEY_W and action == glfw.PRESS:
        forward = True
    elif key == glfw.KEY_W and action == glfw.RELEASE:
        forward = False
    if key == glfw.KEY_S and action == glfw.PRESS:
        backward = True
    elif key == glfw.KEY_S and action == glfw.RELEASE:
        backward = False
    if key == glfw.KEY_A and action == glfw.PRESS:
        left = True
    elif key == glfw.KEY_A and action == glfw.RELEASE:
        left = False
    if key == glfw.KEY_D and action == glfw.PRESS:
        right = True
    elif key == glfw.KEY_D and action == glfw.RELEASE:
        right = False


# the mouse position callback function
def mouse_look_clb(window, xpos, ypos):
    global first_mouse, lastX, lastY

    if first_mouse:
        lastX, lastY = xpos, ypos
        first_mouse = False
    xoffset = xpos - lastX
    yoffset = lastY - ypos

    lastX = xpos
    lastY = ypos
    mycam.process_mouse_movement(xoffset, yoffset)

