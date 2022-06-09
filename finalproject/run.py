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



def drawer(index, given_indices, pos):
    glBindVertexArray(VAO[index])
    glBindTexture(GL_TEXTURE_2D, textures[index])
    glUniformMatrix4fv(model_location, 1, GL_FALSE, pos)
    glDrawArrays(GL_TRIANGLES, 0, given_indices)


def binder(object_buffer, index):
    glBindVertexArray(VAO[index])
    glBindBuffer(GL_ARRAY_BUFFER, VBO[index])
    glBufferData(GL_ARRAY_BUFFER, object_buffer.nbytes, object_buffer, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, object_buffer.itemsize * 8, ctypes.c_void_p(0))

    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, object_buffer.itemsize * 8, ctypes.c_void_p(12))

    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, object_buffer.itemsize * 8, ctypes.c_void_p(20))
    glEnableVertexAttribArray(2)



def getFileContents(filename):
    p = os.path.join(os.getcwd(), "shaders", filename)
    return open(p, 'r').read()
# glfw callback functions


def window_resize(window, width, height):
    glViewport(0, 0, width, height)
    projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 100)
    glUniformMatrix4fv(projection_location, 1, GL_FALSE, projection)


# initializing glfw library
if not glfw.init():
    raise Exception("glfw can not be initialized!")

# creating the window
window = glfw.create_window(WIDTH, HEIGHT, "My OpenGL window", None, None)

# check if window was created
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

glfw.set_window_size_callback(window, window_resize)
glfw.set_cursor_pos_callback(window, mouse_look_clb)
glfw.set_key_callback(window, key_input_clb)
glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

glfw.make_context_current(window)

dog_indices, dog_buffer = ObjectLoader("objects/dog.obj").load_the_model()
wall_indices, wall_buffer = ObjectLoader("objects/wall.obj").load_the_model()
fence_indices, fence_buffer = ObjectLoader("objects/fence.obj").load_the_model()
roof_indices, roof_buffer = ObjectLoader("objects/tara.obj").load_the_model()
windowsanddoor_indices, windowsanddoor_buffer = ObjectLoader("objects/windowsanddoor.obj").load_the_model()
beranda_indices, beranda_buffer = ObjectLoader("objects/brenda.obj").load_the_model()
outdoor_indices, outdoor_buffer = ObjectLoader("objects/outdoor.obj").load_the_model()
ground_indices, ground_buffer = ObjectLoader("objects/ground.obj").load_the_model()
gomma_indices, gomma_buffer = ObjectLoader("objects/gomma.obj").load_the_model()
poll_indices, poll_buffer = ObjectLoader("objects/poll.obj").load_the_model()
bowl_indices, bowl_buffer = ObjectLoader("objects/bowl.obj").load_the_model()
doorbench_indices, doorbench_buffer = ObjectLoader("objects/doorbench.obj").load_the_model()
roofdecor_indices, roofdecor_buffer = ObjectLoader("objects/roofdecor.obj").load_the_model()
ceil_indices, ceil_buffer = ObjectLoader("objects/roofhelper.obj").load_the_model()
mestawot_indices, mestawot_buffer = ObjectLoader("objects/mestawot.obj").load_the_model()
roof_bottom_indices, roof_bottom_buffer = ObjectLoader("objects/floorr2.obj").load_the_model()


shader = compileProgram(compileShader(getFileContents("models.vertex.shader"), GL_VERTEX_SHADER), compileShader(getFileContents("models.fragment.shader"), GL_FRAGMENT_SHADER))

VAO = glGenVertexArrays(20)
VBO = glGenBuffers(20)
# **********************    bind here         *****************************
#   bind vertices, texture and normal
binder(dog_buffer, 0)
binder(wall_buffer, 1)
binder(fence_buffer, 2)
binder(roof_buffer, 3)
binder(windowsanddoor_buffer, 4)
binder(beranda_buffer, 5)
binder(outdoor_buffer, 6)
binder(ground_buffer, 7)
binder(gomma_buffer, 8)
binder(poll_buffer, 9)
binder(bowl_buffer, 10)
binder(doorbench_buffer, 11)
binder(roofdecor_buffer, 12)
binder(ceil_buffer, 13)
binder(mestawot_buffer, 14)
binder(roof_bottom_buffer, 15)


# **********************   load texture        ****************************
textures = glGenTextures(20)
load_texture("images/dog_COL.png", textures[0])
load_texture("images/bricks.jpg", textures[1])
load_texture("images/fence.png", textures[2])
load_texture("images/roof.png", textures[3])
load_texture("images/fence.png", textures[4])
load_texture("images/beranda.jpg", textures[5])
load_texture("images/outdoor.png", textures[6])
load_texture("images/ground.jpg", textures[7])
load_texture("images/black.jpg", textures[8])
load_texture("images/poll1.png", textures[9])
load_texture("images/blue.png", textures[10])
load_texture("images/black.jpg", textures[11])
load_texture("images/frontend-large.jpg", textures[12])
load_texture("images/Map 73.jpg", textures[13])
load_texture("images/mestawot.png", textures[14])
load_texture("images/myfloortex.jpg", textures[15])


glUseProgram(shader)
glClearColor(0, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

projection = pyrr.matrix44.create_perspective_projection_matrix(45, WIDTH / HEIGHT, 0.1, 100)

dog_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
wall_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
fence_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
roof_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
windowanddoor_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
beranda_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
outdoor_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
ground_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
gomma_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
poll_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
bowl_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
doorbench_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
roofdecor_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
ceil_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
mestawot_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
roof_bottom_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))



model_location = glGetUniformLocation(shader, "model")
projection_location = glGetUniformLocation(shader, "projection")
view_location = glGetUniformLocation(shader, "view")

glUniformMatrix4fv(projection_location, 1, GL_FALSE, projection)
