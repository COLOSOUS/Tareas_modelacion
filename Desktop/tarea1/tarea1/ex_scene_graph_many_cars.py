# coding=utf-8
"""
Daniel Calderon, CC3501, 2019-1
Drawing many cars using a scene graph
"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import transformations as tr
import scene_graph_1b as sg
import sys

# We will use 32 bits data, so an integer has 4 bytes
# 1 byte = 8 bits
INT_BYTES = 4


# A class to store the application control
class Controller:
    fillPolygon = True


# we will use the global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_ESCAPE:
        sys.exit()

    else:
        print('Unknown key')


def createQuad(r, g, b):

    # Here the new shape will be stored
    gpuShape = sg.GPUShape()

    # Defining locations and colors for each vertex of the shape    
    vertexData = np.array([
    #   positions        colors
        -0.5, -0.5, 0.0,  r, g, b,
         0.5, -0.5, 0.0,  r, g, b,
         0.5,  0.5, 0.0,  r, g, b,
        -0.5,  0.5, 0.0,  r, g, b
    # It is important to use 32 bits data
        ], dtype = np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0, 1, 2,
         2, 3, 0], dtype= np.uint32)

    gpuShape.size = len(indices)

    # VAO, VBO and EBO and  for the shape
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    # Vertex data must be attached to a Vertex Buffer Object (VBO)
    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertexData) * INT_BYTES, vertexData, GL_STATIC_DRAW)

    # Connections among vertices are stored in the Elements Buffer Object (EBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * INT_BYTES, indices, GL_STATIC_DRAW)

    return gpuShape


def createCar():
    
    # Cheating a single wheel
    wheel = sg.SceneGraphNode("wheel")
    wheel.transform = tr.uniformScale(0.2)
    wheel.childs += [createQuad(0,0,0)]

    wheelRotation = sg.SceneGraphNode("wheelRotation")
    wheelRotation.childs += [wheel]

    # Instanciating 2 wheels, for the front and back parts
    frontWheel = sg.SceneGraphNode("frontWheel")
    frontWheel.transform = tr.translate(0.3,-0.3,0)
    frontWheel.childs += [wheelRotation]

    backWheel = sg.SceneGraphNode("backWheel")
    backWheel.transform = tr.translate(-0.3,-0.3,0)
    backWheel.childs += [wheelRotation]
    
    # Creating the chasis of the car
    chasis = sg.SceneGraphNode("chasis")
    chasis.transform = tr.scale(1,0.5,1)
    chasis.childs += [createQuad(1,0,0)]

    car = sg.SceneGraphNode("car")
    car.childs += [chasis]
    car.childs += [frontWheel]
    car.childs += [backWheel]

    traslatedCar = sg.SceneGraphNode("traslatedCar")
    traslatedCar.transform = tr.translate(0,0.3,0)
    traslatedCar.childs += [car]

    return traslatedCar

def createCars(N):

    # First we scale a car
    scaledCar = sg.SceneGraphNode("scaledCar")
    scaledCar.transform = tr.uniformScale(0.15)
    scaledCar.childs += [createCar()] # Re-using the previous function

    # Root node where all cars will be added
    cars = sg.SceneGraphNode("cars")

    # Each car is created and then added to the root 'cars' node
    baseName = "scaledCar_"
    for i in range(N):
        # A new node is only locating a scaledCar in the scene depending on index i
        newNode = sg.SceneGraphNode(baseName + str(i))
        newNode.transform = tr.translate(0.4 * i - 0.9, 0.9 - 0.4 * i, 0)
        newNode.childs += [scaledCar]

        # Now this car is added to the 'cars' scene graph
        cars.childs += [newNode]

    return cars


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Cars via scene graph", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program (pipeline) with both shaders
    shaderProgram = sg.basicShaderProgram()
    
    # Telling OpenGL to use our shader program
    glUseProgram(shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # Creating shapes on GPU memory
    cars = createCars(5)

    # Querying the position of "scaled_car_2"
    car2Position = sg.findPosition(cars, "scaledCar_1", tr.identity())
    print("car2Position =", car2Position)

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Modifying only a specific node in the scene graph
        wheelRotationNode = sg.findNode(cars, "wheelRotation")
        theta = -10 * glfw.get_time()
        wheelRotationNode.transform = tr.rotationZ(theta)

        # Modifying only car 3
        car3 = sg.findNode(cars, "scaledCar_3")
        car3.transform = tr.translate(0.3, 0.5 * np.sin(0.1 * theta), 0)

        # Uncomment to see the position of scaledCar_3, it will fill your terminal
        #print("car3Position =", sg.findPosition(cars, "scaledCar_3", tr.identity()))

        # Drawing the Car
        sg.drawSceneGraphNode(cars, shaderProgram, tr.identity())

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    
    glfw.terminate()