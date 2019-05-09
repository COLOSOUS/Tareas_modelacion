# coding=utf-8
"""
Crea un cilindro en 3D.

@author ppizarror
"""

# Library imports
import glfw
from OpenGL.GL import *
import sys

import lib.transformations2 as tr2
import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.camera as cam
from lib.mathlib import Point3
import numpy as np

# Import extended shapes
import lib.basic_shapes_extended as bs_ext

# Import lights
import lib.lights as light
import lib.catrom as catrom


# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True


# Global controller as communication with the callback function
controller = Controller()

# Create camera
camera = cam.CameraR(r=25, center=Point3())
camera.move_center_z(3)
camera2 = cam.CameraR(r=10, center=Point3())
camera3 = cam.CameraR(r=3, center=Point3())
camera3.move_center_z(3)
camera3.rotate_theta(30)


camera4 = cam.CameraR(r=5, center=Point3())
camera4.rotate_phi(20)
camera4.rotate_theta(-20)
camera5 = cam.CameraR(r=17, center=Point3())
camera5.move_center_z(7)
camera.set_r_vel(0.3)


# noinspection PyUnusedLocal
def on_key(window_obj, key, scancode, action, mods):
    global controller
    global obj_light

    if action == glfw.REPEAT or action == glfw.PRESS:
        # Move the camera position
        if key == glfw.KEY_LEFT:
            camera.rotate_phi(-4)
        elif key == glfw.KEY_RIGHT:
            camera.rotate_phi(4)


        # Move the center of the camera
        elif key == glfw.KEY_K:
            b=1
        elif key == glfw.KEY_L:
            b=0
        #elif key == glfw.KEY_K:
          #  camera.move_center_x(0.05)
        #elif key == glfw.KEY_J:
         #   camera.move_center_y(-0.05)
        #elif key == glfw.KEY_L:
           # camera.move_center_y(0.05)
        #elif key == glfw.KEY_U:
         #   camera.move_center_z(-0.05)
        #elif key == glfw.KEY_O:
         #   camera.move_center_z(0.05)

    if action != glfw.PRESS:
        return

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = 1
    elif key == glfw.KEY_1:
        controller.fillPolygon = 2
    elif key == glfw.KEY_2:
        controller.fillPolygon = 3
    elif key == glfw.KEY_3:
        controller.fillPolygon = 4
    elif key == glfw.KEY_4:
        controller.fillPolygon = 5

    elif key == glfw.KEY_ESCAPE:
        sys.exit()

    elif key == glfw.KEY_Z:
        obj_light.change_color(np.random.random(), np.random.random(), np.random.random())


if __name__ == '__main__':

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 1200
    height = 1000

    window = glfw.create_window(width, height, 'Cilindro bonito', None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Creating shader programs for textures and for colores
    colorShaderProgram = es.SimpleModelViewProjectionShaderProgram()
    phongPipeline = es.SimplePhongShaderProgram()
    textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.55, 0.55, 0.95, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Create models
    gpuAxis = es.toGPUShape(bs.createAxis(1))
    # Bottom plane
    aa=3.5
    s1 = (1*aa, -1*aa, -0.1)
    s2 = (-1*aa, -1*aa, -0.1)
    s3 = (-1*aa, 1*aa,-0.1)
    s4 = (1*aa, 1*aa, -0.1)
    gpuTexturePlane = es.toGPUShape(bs_ext.create4VertexTexture('c.jpg', s1, s2, s3, s4), GL_REPEAT, GL_LINEAR)
    obj_planeB = bs_ext.AdvancedGPUShape(gpuTexturePlane, shader=textureShaderProgram)
    obj_planeB.rotationZ(np.pi)
    obj_planeB.scale(2.5, 2.5, 2.5)

    s1 = (0.9*aa, -0.45*aa, 0)
    s2 = (-0.9*aa, -0.45*aa, 0)
    s3 = (-0.9*aa, 0.5*aa, 0)
    s4 = (0.9*aa, 0.5*aa, 0)
    gpuTexturePlane = es.toGPUShape(bs_ext.create4VertexTexture('p.jpg', s1, s2, s3, s4), GL_REPEAT, GL_LINEAR)
    obj_planeB2 = bs_ext.AdvancedGPUShape(gpuTexturePlane, shader=textureShaderProgram)
    obj_planeB2.rotationZ(np.pi)
    obj_planeB2.scale(1, 2, 1)
    obj_axis = bs_ext.AdvancedGPUShape(gpuAxis, shader=colorShaderProgram)

    vertices = [[3, 0], [2.9, 0.4], [0.8, 0.8], [0, 0]]
    curve = catrom.getSplineFixed(vertices, 30)
    obj_planeL = bs_ext.createColorPlaneFromCurve(curve, True, 0.6, 0.6, 0.6, center=(0, 0))
    obj_planeL.rotationZ(np.pi/2)
    obj_planeL.translate(0, 0, 0.01)
    obj_planeL.setShader(colorShaderProgram)
    obj_planeR1 = obj_planeL.clone()
    obj_planeR1.rotationZ(np.pi / 2)
    obj_planeR2 = obj_planeR1.clone()
    obj_planeR2.rotationZ(np.pi / 2)
    obj_planeR3 = obj_planeR2.clone()
    obj_planeR3.rotationZ(np.pi / 2)
    ################################################
    # Textured plane
    p1=0.3
    s1 = (p1, 0, 0)
    s2 = (-p1, 0, 0)
    s3 = (-p1, 10, 0)
    s4 = (p1, 10, 0)
    gpuTexturePlane = es.toGPUShape(bs_ext.create4VertexTexture('p1.jpg', s1, s2, s3, s4), GL_REPEAT, GL_LINEAR)
    obj_planeP1 = bs_ext.AdvancedGPUShape(gpuTexturePlane, shader=textureShaderProgram)
    obj_planeP1.rotationX(np.pi / 2)
    obj_planeP2 = obj_planeP1.clone()
    obj_planeP2.rotationZ(np.pi / 2)
    obj_planeP3 = obj_planeP2.clone()
    obj_planeP3.rotationZ(np.pi / 2)
    obj_planeP4 = obj_planeP3.clone()
    obj_planeP4.rotationZ(np.pi / 2)
    obj_planeP1.rotationZ(np.pi / 2)
    obj_planeP2.rotationZ(np.pi / 2)
    obj_planeP3.rotationZ(np.pi / 2)
    obj_planeP4.rotationZ(np.pi / 2)


    obj_planeP1.translate(p1, 0, 0)
    obj_planeP2.translate(0, p1, 0)
    obj_planeP3.translate(-p1, 0, 0)
    obj_planeP4.translate(0,-p1, 0)
    obj_plane_pp1=obj_planeP1.clone()
    obj_plane_pp2=obj_planeP2.clone()
    obj_plane_pp3=obj_planeP3.clone()
    obj_plane_pp4=obj_planeP4.clone()
    obj_plane_pp1.scale(1.2, 0.6, 1)
    obj_plane_pp2.scale(1.2, 0.6, 1)
    obj_plane_pp3.scale(1.2, 0.6, 1)
    obj_plane_pp4.scale(1.2, 0.6, 1)

    obj_plane_ppp1=obj_plane_pp1.clone()
    obj_plane_ppp2=obj_plane_pp2.clone()
    obj_plane_ppp3=obj_plane_pp3.clone()
    obj_plane_ppp4=obj_plane_pp4.clone()

    obj_plane_pp1.translate(0, -0.35, -1)
    obj_plane_pp2.translate(0, -0.35, -1)
    obj_plane_pp3.translate(0, -0.35, -1)
    obj_plane_pp4.translate(0, -0.35, -1)

    obj_plane_ppp1.translate(0, 0.35, -1)
    obj_plane_ppp2.translate(0, 0.35, -1)
    obj_plane_ppp3.translate(0, 0.35, -1)
    obj_plane_ppp4.translate(0, 0.35, -1)

    ################################################
    ################################################
    # Textured plane
    p12 =0.55
    s1 = (p12, 0, 0)
    s2 = (-p12, 0, 0)
    s3 = (-p12, 3, 0)
    s4 = (p12, 3, 0)
    gpuTexturePlane = es.toGPUShape(bs_ext.create4VertexTexture('p8.jpg', s1, s2, s3, s4), GL_REPEAT, GL_LINEAR)
    obj_planeP12 = bs_ext.AdvancedGPUShape(gpuTexturePlane, shader=textureShaderProgram)
    obj_planeP12.rotationX(np.pi / 2)
    obj_planeP22 = obj_planeP12.clone()
    obj_planeP22.rotationZ(np.pi / 2)
    obj_planeP32 = obj_planeP22.clone()
    obj_planeP32.rotationZ(np.pi / 2)
    obj_planeP42 = obj_planeP32.clone()
    obj_planeP42.rotationZ(np.pi / 2)
    obj_planeP12.rotationZ(np.pi / 2)
    obj_planeP22.rotationZ(np.pi / 2)
    obj_planeP32.rotationZ(np.pi / 2)
    obj_planeP42.rotationZ(np.pi / 2)

    obj_planeP12.translate(p12, 0, 0)
    obj_planeP22.translate(0, p12, 0)
    obj_planeP32.translate(-p12, 0, 0)
    obj_planeP42.translate(0, -p12, 0)

    ################################################
    ################################################
    # Textured plane
    t3 = 0.15
    s1 = (t3, 0, 0)
    s2 = (-t3, 0, 0)
    s3 = (-t3, 15, 0)
    s4 = (t3, 15, 0)
    gpuTexturePlane = es.toGPUShape(bs_ext.create4VertexTexture('p2.jpg', s1, s2, s3, s4), GL_REPEAT, GL_LINEAR)
    obj_planet12a = bs_ext.AdvancedGPUShape(gpuTexturePlane, shader=textureShaderProgram)
    obj_planet12a.rotationX(np.pi / 2)
    obj_planet22a = obj_planet12a.clone()
    obj_planet22a.rotationZ(np.pi / 2)
    obj_planet32a = obj_planet22a.clone()
    obj_planet32a.rotationZ(np.pi / 2)
    obj_planet42a = obj_planet32a.clone()
    obj_planet42a.rotationZ(np.pi / 2)
    obj_planet12a.rotationZ(np.pi / 2)
    obj_planet22a.rotationZ(np.pi / 2)
    obj_planet32a.rotationZ(np.pi / 2)
    obj_planet42a.rotationZ(np.pi / 2)

    obj_planet12a.translate(p12, 0, 0)
    obj_planet22a.translate(0, p12, 0)
    obj_planet32a.translate(-p12, 0, 0)
    obj_planet42a.translate(0, -p12, 0)

    ################################################
    ################################################
    # Textured plane
    p12p = 0.55
    s1 = (-p12p, -p12p, 0)
    s2 = (p12p, -p12p, 0)
    s3 = (p12p, p12p, 0)
    s4 = (-p12p, p12p, 0)
    gpuTexturePlane = es.toGPUShape(bs_ext.create4VertexTexture('p3.jpg', s1, s2, s3, s4), GL_REPEAT, GL_LINEAR)
    obj_planeP12p = bs_ext.AdvancedGPUShape(gpuTexturePlane, shader=textureShaderProgram)


    obj_planeP12p.translate(0, 0, 3)


    ################################################
    ################################################
    # Textured plane
    p12p = 0.5
    s1 = (-p12p, -p12p, 0)
    s2 = (p12p, -p12p, 0)
    s3 = (p12p, p12p, 0)
    s4 = (-p12p, p12p, 0)
    gpuTexturePlane = es.toGPUShape(bs_ext.create4VertexTexture('p4.jpg', s1, s2, s3, s4), GL_REPEAT, GL_LINEAR)
    obj_planeP12tt = bs_ext.AdvancedGPUShape(gpuTexturePlane, shader=textureShaderProgram)


    obj_planeP12tt.translate(0, 0, 9)
    obj_planeP12tt.scale(0.75, 1, 1)
    p12p = 0.3
    s1 = (-p12p, -p12p, 0)
    s2 = (p12p, -p12p, 0)
    s3 = (p12p, p12p, 0)
    s4 = (-p12p, p12p, 0)
    gpuTexturePlane = es.toGPUShape(bs_ext.create4VertexTexture('p4.jpg', s1, s2, s3, s4), GL_REPEAT, GL_LINEAR)
    obj_planeP12ttt = bs_ext.AdvancedGPUShape(gpuTexturePlane, shader=textureShaderProgram)

    obj_planeP12ttt.translate(0, 0, 10)
    obj_planeP12ttt.scale(1, 1, 1)


    ################################################
    # Create cilynder, the objective is create many cuads from the bottom, top and
    # mantle. The cilynder is parametrized using an angle theta, a radius r and
    # the height
    h = 1
    r = 0.05

    # Latitude and longitude of the cylinder, latitude subdivides theta, longitude
    # subdivides h
    lat = 20
    lon = 20

    # Angle step
    dang = 2 * np.pi / lat

    # Color
    color = {
        'r': 100/255,  # Red
        'g': 30/255,  # Green
        'b': 22/255,  # Blue
    }

    cylinder_shape = []  # Store shapes

    # Create mantle
    for i in range(lon):  # Vertical component
        for j in range(lat):  # Horizontal component

            # Angle on step j
            ang = dang * j

            # Here we create a quad from 4 vertices
            #
            #    a/---- b/
            #    |      |
            #    d ---- c
            a = [r * np.cos(ang), r * np.sin(ang), h / lon * (i + 1)]
            b = [r * np.cos(ang + dang), r * np.sin(ang + dang), h / lon * (i + 1)]
            c = [r * np.cos(ang + dang), r * np.sin(ang + dang), h / lon * i]
            d = [r * np.cos(ang), r * np.sin(ang), h / lon * i]

            # Create quad
            shape = bs_ext.create4VertexColorNormal(a, b, c, d, color['r'], color['g'], color['b'])
            cylinder_shape.append(es.toGPUShape(shape))

    # Add the two covers
    for j in range(lat):
        ang = dang * j

        # Bottom
        a = [0, 0, 0]
        b = [r * np.cos(ang), r * np.sin(ang), 0]
        c = [r * np.cos(ang + dang), r * np.sin(ang + dang), 0]
        shape = bs_ext.createTriangleColorNormal(c, b, a, color['r'], color['g'], color['b'])
        cylinder_shape.append(es.toGPUShape(shape))

        # Top
        a = [0, 0, h]
        b = [r * np.cos(ang), r * np.sin(ang), h]
        c = [r * np.cos(ang + dang), r * np.sin(ang + dang), h]
        shape = bs_ext.createTriangleColorNormal(c, b, a, color['r'], color['g'], color['b'])
        cylinder_shape.append(es.toGPUShape(shape))

    # Create cylinder object
    obj_cylinder = bs_ext.AdvancedGPUShape(cylinder_shape, shader=phongPipeline)
    obj_cylinder.translate(0,0,10)


    # Create light
    obj_light = light.Light(shader=phongPipeline, position=[3, 3, 3], color=[1, 1, 1])

    # Main execution loop
    view = camera.get_view()
    controller.fillPolygon == 1


    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Create projection
        # projection = tr2.ortho(-1, 1, -1, 1, 0.1, 100)
        projection = tr2.perspective(45, float(width) / float(height), 0.1, 100)

        # Get camera view matrix


        # Place light
        obj_light.place()

        # Draw objects
        obj_axis.draw(view, projection, mode=GL_LINES)
        obj_cylinder.draw(view, projection)
        obj_planeB.draw(view, projection)
        obj_planeB2.draw(view, projection)
        obj_planeL.draw(view, projection)
        obj_planeR1.draw(view, projection)
        obj_planeR2.draw(view, projection)
        obj_planeR3.draw(view, projection)
        obj_planeP1.draw(view, projection)
        obj_planeP2.draw(view, projection)
        obj_planeP3.draw(view, projection)
        obj_planeP4.draw(view, projection)
        obj_planeP12.draw(view, projection)
        obj_planeP22.draw(view, projection)
        obj_planeP32.draw(view, projection)
        obj_planeP42.draw(view, projection)
        obj_plane_pp1.draw(view, projection)
        obj_plane_pp2.draw(view, projection)
        obj_plane_pp3.draw(view, projection)
        obj_plane_pp4.draw(view, projection)
        obj_plane_ppp1.draw(view, projection)
        obj_plane_ppp2.draw(view, projection)
        obj_plane_ppp3.draw(view, projection)
        obj_plane_ppp4.draw(view, projection)
        ##################################

###############################
        obj_planeP12ttt.draw(view, projection)
        obj_planeP12tt.draw(view, projection)
        obj_planeP12p.draw(view, projection)
        if controller.fillPolygon == 1:
            view = camera.get_view()
        if controller.fillPolygon==2:
           view = camera2.get_view()
        if controller.fillPolygon==3:
           view = camera3.get_view()
        if controller.fillPolygon==4:
           view = camera4.get_view()
        if controller.fillPolygon==5:
           view = camera5.get_view()





        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen
        glfw.swap_buffers(window)

    glfw.terminate()
