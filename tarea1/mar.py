import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import transformations as tr
import scene_graph_1b as sg
import sys
import time

INT_BYTES = 4


# A class to store the application control
class Controller:
    new = False
    def __init__(self):
        self.leftClickOn = False
        self.theta = 0.0
        self.mousePos = (0.0, 0.0)


# we will use the global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return

    global controller

    if key == glfw.KEY_ESCAPE:
        sys.exit()
    elif key == glfw.KEY_ENTER:
        controller.new = not controller.new
        print("Nuevo pescadito")

    else:
        print('Unknown key')
def cursor_pos_callback(window, x, y):
    global controller
    controller.mousePos = (x,y)
def mouse_button_callback(window, button, action, mods):

    global controller

    """
    glfw.MOUSE_BUTTON_1: left click
    glfw.MOUSE_BUTTON_2: right click
    glfw.MOUSE_BUTTON_3: scroll click
    """

    if (action == glfw.PRESS or action == glfw.REPEAT):
        if (button == glfw.MOUSE_BUTTON_1):
            controller.leftClickOn = True


        if (button == glfw.MOUSE_BUTTON_2):
            None




    elif (action ==glfw.RELEASE):
        if (button == glfw.MOUSE_BUTTON_1):
            controller.leftClickOn = False


def scroll_callback(window, x, y):

    print("Mouse scroll:", x, y)
def basicShaderProgram():

    # Defining shaders for our pipeline
    vertex_shader = """
    #version 130
    in vec3 position;
    in vec3 color;

    out vec3 fragColor;

    uniform mat4 transform;

    void main()
    {
        fragColor = color;
        gl_Position = transform * vec4(position, 1.0f);
    }
    """

    fragment_shader = """
    #version 130

    in vec3 fragColor;
    out vec4 outColor;

    void main()
    {
        outColor = vec4(fragColor, 1.0f);
    }
    """

    # Assembling the shader program (pipeline) with both shaders
    shaderProgram = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    return shaderProgram


def drawShape(shaderProgram, shape, transform):
    # Binding the proper buffers
    glBindVertexArray(shape.vao)
    glBindBuffer(GL_ARRAY_BUFFER, shape.vbo)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, shape.ebo)

    # updating the new transform attribute
    glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "transform"), 1, GL_FALSE, transform)

    # Describing how the data is stored in the VBO
    position = glGetAttribLocation(shaderProgram, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)

    color = glGetAttribLocation(shaderProgram, "color")
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)

    # This line tells the active shader program to render the active element buffer with the given size
    glDrawElements(GL_TRIANGLES, shape.size, GL_UNSIGNED_INT, None)


# A simple class container to reference a shape on GPU memory
class GPUShape:
    def __init__(self):
        self.vao = 0
        self.vbo = 0
        self.ebo = 0
        self.size = 0
######################################################


def createQuad2():
    # Here the new shape will be stored
    gpuShape = sg.GPUShape()

    # Defining locations and colors for each vertex of the shape
    vertexData = np.array([
        #   positions        colors
        -0.3, -0.2, 0.0, 1, 0.2*207 / 255.0,0.2* 96 / 255.0,
        0.7, -0.2, 0.0, 0.2*168 / 255.0, 0.2*121 / 255.0, 0.2*11 / 255.0,
        0.2, 0.7, 0.0, 0.2*229 / 255.0, 0.2*214 / 255.0,0.2* 142 / 255.0,

        0.7, -0.2, 0.0, 0.2*122 / 255.0, 0.2*89 / 255.0,0.2* 13 / 255.0,
        0.2, 0.7, 0.0, 0.2*122 / 255.0,0.2* 89 / 255.0, 0.2*13 / 255.0,
        0.9, -0.1, 0.0, 0.2*122 / 255.0,0.2* 89 / 255.0,0.2* 13 / 255.0
        # It is important to use 32 bits data
    ], dtype=np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0, 1, 2,
         3, 4, 5], dtype=np.uint32)

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
def createQuad(r, g, b):
    # Here the new shape will be stored
    gpuShape = sg.GPUShape()

    # Defining locations and colors for each vertex of the shape
    vertexData = np.array([
        #   positions        colors
        -0.5, 0.45, 0.0, r, g, b,
        -0.5+0.33, -0.05, 0.0, r, g, b,
        -0.5+0.33+0.33, -0.45, 0.0, r, g, b,
        -0.5 + 0.33 +0.33+0.33, 0, 0.0, r, g, b
        - 0.5 + 0.33 + 0.33, 0.45, 0.0, r, g, b,
        -0.5 + 0.33, 0.05, 0.0, r, g, b,
        - 0.5 , 0.45, 0.0, r, g, b,
        # It is important to use 32 bits data
    ], dtype=np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0,6, 2,0], dtype=np.uint32)

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
def createQuad3(r, g, b):
    # Here the new shape will be stored
    gpuShape = sg.GPUShape()
    c = 0.8
    o =0.2

    # Defining locations and colors for each vertex of the shape
    vertexData = np.array([

        #   positions        colors
        -0.75, -0.45-0.5, 0.0, r*o, g*o, b*o,
        -1 + 0.33, 1, 0.0, r*c, g*c, b*c,
        -0.33, -0.1+0.5, 0.0, r, g, b,
        1, 0.1, 0.0, r, g, b,

        - 1+ 0.33 + 0.33, 0.45+0.5, 0.0, r, g, b,
        -1 + 0.33, 0.05, 0.0, r*c, g*c, b*c,
        - 1, 0.45-0.5, 0.0, r, g, b,
        0.75, - 0.5, 0.0, r*o, g*o, b*o,
        # It is important to use 32 bits data
    ], dtype=np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0, 1, 2,
         3, 4, 5, 6,
         7, 4, 5,

         ], dtype=np.uint32)

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


def sea_1():
    # Here the new shape will be stored
    gpuShape = sg.GPUShape()
    # Defining locations and colors for each vertex of the shape
    vertexData = np.array([
        #   positions  colors
        -1, -1, 0, 0, 0, 102 / 255,
        1, -1, 0, 0, 0, 102 / 255,
        1, 1, 0, 0.5, 0.5, 1,
        -1, 1, 0, 0.5, 0.5, 1
        # It is important to use 32 bits data
    ], dtype=np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0, 1, 2,
         2, 3, 0], dtype=np.uint32)

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


def arena_1():
    # Here the new shape will be stored
    gpuShape = sg.GPUShape()

    # Defining locations and colors for each vertex of the shape
    vertexData = np.array([
        #   positions    colors
        -1, -1, 0, 160 / 255.0, 134 / 255.0, 73 / 255.0,
        1, -1, 0, 168 / 255.0, 121 / 255.0, 11 / 255.0,
        1, -0.55, 0, 244 / 255.0, 223 / 255.0, 66 / 255.0,
        -1, -0.45, 0, 1, 207 / 255.0, 96 / 255.0
        # It is important to use 32 bits data
    ], dtype=np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0, 1, 2,
         3, 1, 0], dtype=np.uint32)

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


def createfish1():
    fish1 = sg.SceneGraphNode("fish1")
    fish1.transform = tr.scale(1, 0.5, 1)

    fish1.childs += [createQuad3(1, 0.2, 0.3)]



    return fish1


def createfish2():
    fish2 = sg.SceneGraphNode("fish2")
    fish2.transform = tr.scale(1, 0.5, 1)
    fish2.childs += [createQuad3(0.5, 1, 0.3)]
    return fish2


def createfish3():
    fish3 = sg.SceneGraphNode("fish3")
    fish3.transform = tr.scale(1, 0.5, 1)
    fish3.childs += [createQuad3(0.2, 0.66, 0.5)]
    return fish3


def createburbuja():
    burbuja = sg.SceneGraphNode("burbuja")
    burbuja.transform = tr.scale(1, 0.5, 1)
    burbuja.childs += [0.75, 0.75, 1]
    return burbuja
def createrock():
    rock = sg.SceneGraphNode("rock")
    rock.transform = tr.scale(1, 0.25, 1)
    rock.childs += [createQuad2()]
    return rock



def createalga():
    # Cheating a single wheel

    alga = sg.SceneGraphNode("alga")
    alga.transform = tr.scale(0.03,0.15,0)
    alga.childs += [createQuad(0, 0.25, 0)]

    #algaRotation_1 = sg.SceneGraphNode("algaRotation_1")
    #algaRotation_1.childs += [alga]
    #algaRotation_2 = sg.SceneGraphNode("algaRotation_2")
    #algaRotation_2.childs += [alga]

    #upalga = sg.SceneGraphNode("upalga")
    #upalga.transform = tr.translate(0,0.0125, 0)
    #upalga.childs += ["algaRotation_1"]

    #downalga = sg.SceneGraphNode("downalga")
    #downalga.transform = tr.translate(0, 0, 0)
    #downalga.childs += ["algaRotation_2"]
    #alga.child += [upalga]
    #alga.child += [downalga]

    return alga
def suelo(n):
    roca = sg.SceneGraphNode("roca")
    roca.transform = tr.uniformScale(0.4)
    roca.childs += [createrock()]
    rocas = sg.SceneGraphNode("rocas")
    baseName0 = "scaledrocks_"


    for i in range(n):
        newNode0 = sg.SceneGraphNode(baseName0 + str(i))
        xx = np.random.rand(1)
        yy = np.random.rand(1)
        newNode0.transform = tr.translate(-0.9 + xx * 0.2 + 0.15 * (1 + i), - 1 + yy * 0.002+0.025, 0)
        newNode0.childs += [roca]
        rocas.childs += [newNode0]
    return rocas

def createfishes(N):
    # First we scale a car
    scaledfish = sg.SceneGraphNode("scaledfish")
    scaledfish.transform = tr.uniformScale(0.25)
    scaledfish.childs += [createfish1()]  # Re-using the previous function
    scaledalga = sg.SceneGraphNode("algas")
    scaledalga.transform = tr.uniformScale(5)
    scaledalga.childs += [createalga()]

    # Root node where all cars will be added
    fishes = sg.SceneGraphNode("fishes")
    algas = sg.SceneGraphNode("algas")

    sea = sg.SceneGraphNode("sea")
    agua = sg.SceneGraphNode("agua")
    agua.transform = tr.identity()
    agua.childs += [sea_1()]


    # sea = sg.SceneGraphNode("sea")
    # sea.childs += [sea()]
    arena = sg.SceneGraphNode("arena")
    arena.transform = tr.uniformScale(1)
    arena.childs += [arena_1()]


    n=10






    sea.childs += [agua]
    sea.childs += [arena]
    sea.childs += [algas]
    sea.childs += [fishes]
    sea.childs += [suelo(n)]



###############################################################





















##############################################

    # Each car is created and then added to the root 'cars' node
    baseName = "scaledfishes_"
    baseName2= "scaledalga_"
    baseName3 = "scaledalga2_"
    for i in range(N):
        # A new node is only locating a scaledCar in the scene depending on index i
        newNode = sg.SceneGraphNode(baseName + str(i))
        newNode2 = sg.SceneGraphNode(baseName2 + str(i))
        newNode3 = sg.SceneGraphNode(baseName3 + str(i))

        newNode.transform = tr.translate((0.5-np.random.rand(1))/2, (0.5-np.random.rand(1))/2, 1)
        xx=np.random.rand(1)
        yy=np.random.rand(1)
        newNode3.transform = tr.translate(-1.1 + xx * 0.1 + 0.35 * (1 + i), 0.05 - 0.8 + yy * 0.1 + 0.21, 0)
        newNode2.transform = tr.translate(-1.1+xx*0.1 +0.35*(1+i), 0.05-0.8+yy*0.1,0)




        newNode.childs += [scaledfish]
        newNode2.childs += [scaledalga]
        newNode3.childs += [scaledalga]


        # Now this car is added to the 'cars' scene graph
        fishes.childs += [newNode]
        algas.childs += [newNode2]
        algas.childs += [newNode3]

    return sea
def create_a_fish(N):
    nodei=sg.findNode(world,"fishes")
    scaledfish = sg.SceneGraphNode("scaledfish")
    scaledfish.transform = tr.uniformScale(0.25)
    if (0.33>np.random.rand(1)>0):
        scaledfish.childs += [createfish1()]
    if (0.66>np.random.rand(1) > 0.33):
        scaledfish.childs += [createfish2()]
    if (1>np.random.rand(1) > 0.66):
        scaledfish.childs += [createfish3()]


    node = sg.SceneGraphNode("scaledfishes_"+str(N-1))
    node.transform = tr.translate((0.5 - np.random.rand(1)) / 2, (0.5 - np.random.rand(1)) / 2, 1)
    node.childs += [scaledfish]
    nodei.childs += [node]
def killpecesito(w,nn,x,y):
    #print("Nuevo")
    #print(mousePosY)
    #print(mousePosX)
    #time.sleep(0.5)








    # print(nodep)
    # print(nodeMove.transform)
    for i in range(nn):
        nodo=sg.findNode(w, "scaledfishes_" + str(i))
        nodep = sg.findPosition(w, nodo.name, nodo.transform)
        #print(nodep)
        #print("Nuevo"+str(i))
        #print("pez X")
        #print(nodep[0])
        #print("pez Y")
        #print(nodep[1])
        xx1 = abs(x - nodep[0])
        yy1 = abs(y - nodep[1])
        xx2 = abs(nodep[0]-x)
        yy2 = abs(nodep[1]-y)
        xx=min(xx1,xx2)
        yy = min(yy1, yy2)

        #print(xx)
        #print(yy)

        if (xx<= 0.5 and yy<=0.2 ):
            #print(nodep)
            print("Lo mataste :'(")
            nodo.transform = np.matmul(nodo.transform, tr.uniformScale(0))
            nodo.transform = np.matmul(nodo.transform, tr.translate(10, 10, 10))




        #if ((nodep[1] + 0.13 >= y >= nodep[1] - 0.13) and (nodep[0] + 0.13 >= x >= nodep[0] - 0.13)):





















if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Sea via scene graph", None, None)
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
#############################################cursor
    # Connecting callback functions to handle mouse events:
    # - Cursor moving over the window
    # - Mouse buttons input
    # - Mouse scroll

    glfw.set_cursor_pos_callback(window, cursor_pos_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    # Using the simple shader program from basic_shapes and
    # telling OpenGL to use our shader program
    shaderProgram = basicShaderProgram()
    glUseProgram(shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # Creating shapes on GPU memory
    blueQuad = createQuad(0, 0, 1)
    redQuad = createQuad(1, 0, 0)
    yellowQuad = createQuad(1, 1, 0)
    greenQuad = createQuad(0, 1, 0)

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    t0 = glfw.get_time()


######################################





    world = createfishes(5)
    N = 5




    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    while not glfw.window_should_close(window):
        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        # Using GLFW to check for input events
        glfw.poll_events()
        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)
        # Modifying only a specific node in the scene graph#############
        ######################################
        # While left click is pressed, we have continous rotation movement
        #if controller.leftClickOn:
         #   controller.theta += 4 * dt
         #   if controller.theta >= 2 * np.pi:
          #      controller.theta -= 2 * np.pi
        click = False
        if controller.leftClickOn:
            click = True

        # Drawing the rotating red quad
        drawShape(shaderProgram, redQuad, tr.matmul([
            tr.uniformScale(0.5),
            tr.translate(0.5, 0.0, 0.0),
            tr.rotationZ(controller.theta)
        ]))

        # Getting the mouse location in opengl coordinates
        mousePosX = 2 * (controller.mousePos[0] - width / 2) / width
        mousePosY = 2 * (height / 2 - controller.mousePos[1]) / height
        #print(mousePosX)

        drawShape(shaderProgram, greenQuad, np.matmul(
            tr.uniformScale(0.3),
            tr.translate(mousePosX, mousePosY, 0)
        ))

        # This is another way to work with keyboard inputs
        # Here we request the state of a given key

        # All "non-pressed" keys are in release state

        ######################################



        if (controller.new):
            N=N + 1
            create_a_fish(N)
            print(N)
        controller.new = False

        theta = -0.64* glfw.get_time()

        #algaRotation2Node = sg.findNode(world, "algaRotation2")
        theta2 = 2* glfw.get_time()
        #algaRotation2Node.transform = tr.rotationZ(theta2)
        theta3 =0.00016*np.sin(glfw.get_time())-0.00016*np.cos(glfw.get_time())
        #print(glfw.get_time())
        nodeMove = sg.findNode(world, "agua")
        shea=tr.shearing(0, 0, -1*np.sin( theta), 0.5*np.sin( theta), -1*np.sin( theta), 0.5*np.sin( theta))

        nodeMove.transform =shea
        #nodeMove.transform = np.matmul(nodeMove.transform, shea)
        #Newfish
        #nodeM = sg.findNode(world, "scaledfishes_"+str(N-1))
        #print(nodeM.name)
        #print(nodeM.transform)
        #print(nodeM.childs)





        for i in range(N):
            if (np.random.rand(1)>0):
                v=1
            elif():
                v=-1

            rotp=np.array([
                [1,0,0,v*0.0006*2*1*np.sin(0.5*(np.pi * theta/np.cos(i+1)))],
                [0,1,0,v*0.0006*1.4* np.sin(0.5*(np.pi * theta2*np.sin(i+1)))],
                [0,0,1,0],
                [0,0,0,1]], dtype = np.float32).T

            nodeMove = sg.findNode(world, "scaledfishes_"+str(i))

            nodeMove.transform = np.matmul(nodeMove.transform, rotp)

        if (click):
            #print("click")

            killpecesito(world, N, mousePosX, mousePosY)
            time.sleep(0.01)

            #print(mousePosY)
            #print(mousePosX)




            #print(nodeMove.transform)












           # print("max")
            #
            #print(nodeMove.transform)
        for i in range(5):
            nodeMove2 = sg.findNode(world, "scaledalga_" + str(i))
            nodeMove3 = sg.findNode(world, "scaledalga2_" + str(i))
            rota=tr.rotationZ(theta3)
            rota2 = tr.rotationZ(-theta3)
            movy=tr.translate(-0.3*theta3, 0, 0)

            nodeMove2.transform = np.matmul(rota,nodeMove2.transform)
            nodeMove3.transform = np.matmul(rota2, nodeMove3.transform)
            nodeMove2.transform = np.matmul(movy, nodeMove2.transform)
            nodeMove3.transform = np.matmul(movy, nodeMove3.transform)




            #nodeMove.transform =nodeMove.transform+rotp
            #nodeMove.transform = tr.translate(0.5 * np.sin(0.1 * theta),0.5 * np.sin(0.1 * theta),0)
            #print("max")
            #print(nodeMove.transform)
            #print(np.sin(np.pi * theta))


        # Drawing the sea
        sg.drawSceneGraphNode(world, shaderProgram, tr.identity())



        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)
        #break
    glfw.terminate()
