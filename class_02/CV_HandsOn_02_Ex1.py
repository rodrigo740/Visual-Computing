"""
Visual Computing 2021/2021
Hands On 02 - Colors, 2D Viewing and Transformations

Samuel Silva, 2021
"""
import random
import pygame as pg
import numpy as np
import sys
from numpy import array
from pygame.fastevent import wait
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL import shaders
from OpenGL.arrays import vbo
from glumpy import glm


class VCHelper:
    """ This class provides some helper functions for the Visual Computing class """

    def __init__(self):
        self.windowsize = (0, 0)
        self.shader = None
        self.vao_triangle = None
        self.vbo_triangle = None
        self.tri_top_x = -0.5
        self.clock = pg.time.Clock()

        # windo area projection limits
        self.min_x = self.min_y = -5.0
        self.max_x = self.max_y = 5.0

        # initial values for transformation matrices. All equal to identity
        self.projMatrix = np.identity(4, np.float32)
        self.modelMatrix_triangle = np.identity(4, np.float32)
        self.viewMatrix = np.identity(4, np.float32)
        self.modelMatrix_square = np.identity(4, np.float32)



        # triangle properties
        self.tx = self.ty = self.tz = 0.0
        self.angle = 0.0
        self.scale = self.sx = self.sy = self.sz = 0.3

        # square properties (to use later)
        self.s_tx = 2.0
        self.s_ty = 2.0
        self.s_tz = 0.0
        self.s_angle = 0.0
        self.s_sx = self.s_sy = self.s_sz = 0.2



    def initShaders(self):
        VERTEX_SHADER = shaders.compileShader("""#version 330
            layout (location = 0) in vec3 position;
            
            // code needed here
            layout (location = 1) in vec3 color;
            out vec3 vColor;

            uniform mat4 model;
            uniform mat4 view;
            uniform mat4 projection;

            void main() {
            gl_Position =  vec4(position, 1.0);   
            vColor = vec3(color);
            gl_Position = projection * view * model * vec4(position, 1.0);        

            }""", GL_VERTEX_SHADER)

        result = glGetShaderiv(VERTEX_SHADER, GL_COMPILE_STATUS)
        if not (result):
            raise RuntimeError(glGetShaderInfoLog(VERTEX_SHADER))

        FRAGMENT_SHADER = shaders.compileShader("""#version 330
            out vec4 out_color;
            in vec3 vColor;
            void main() {
                out_color = vec4(vColor,1);
    }""", GL_FRAGMENT_SHADER)

        # just compile the shader program including the two configured shaders
        self.shader = shaders.compileProgram(VERTEX_SHADER, FRAGMENT_SHADER)

        result = glGetProgramiv(self.shader, GL_LINK_STATUS)

        if not (result):
            raise RuntimeError(glGetProgramInfoLog(self.shader))

        glUseProgram(self.shader)

    def initVertexBuffer(self):

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # geometry and color for triangle
        self.triangle_vbo = vbo.VBO(
            array([
                [0, 1, 0, 1, 1, 1],
                [-1, -1, 0, 1, 1, 0],
                [1, -1, 0, 0, 1, 1]
            ], 'f')
        )

        # TODO: define geometry and color for a square

        self.square_vbo = vbo.VBO(
            array([
                [2, 0, 0, 1, 1, 0],
                [2, 1, 0, 1, 1, 0],
                [1, 0, 0, 1, 1, 0],

                [1, 1, 0, 1, 1, 0],
                [2, 1, 0, 1, 1, 0],
                [1, 0, 0, 1, 1, 0],
            ], 'f')
        )


    def render(self):

        glClear(GL_COLOR_BUFFER_BIT)

        self.compute_proj_view_matrix()

        try:

            try:

                # draw triangle
                self.triangle_vbo.bind()

                # the stride is 6 * 4 because we need to jump 6 float numbers,
                # which are 4 bytes each to reach the next vertex. Look at how
                # the vertex buffer object is defined:
                # Vx Vy Vz Cr Cg Cb, Vx, Vy, Vz, ...
                # From Vx to Vx = 6 jumps of 4 bytes each
                glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, None)
                glEnableVertexAttribArray(0)

                glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(3 * 4))
                glEnableVertexAttribArray(1)

                glUseProgram(self.shader)

                # TODO: apply transformation to triangle
                self.compute_transf_matrix_triangle()

                # draw triangle
                glDrawArrays(GL_TRIANGLES, 0, 3)

                #TODO: draw the square
                self.square_vbo.bind()
                glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, None)
                glEnableVertexAttribArray(0)

                glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(3 * 4))
                glEnableVertexAttribArray(1)

                glUseProgram(self.shader)

                self.compute_transf_matrix_square()

                glDrawArrays(GL_TRIANGLES, 0 , 6)

            finally:
                self.triangle_vbo.unbind()
                glDisableClientState(GL_VERTEX_ARRAY)
                glDisableClientState(GL_COLOR_ARRAY)
        finally:
            shaders.glUseProgram(0)

        pg.display.flip()

    def compute_proj_view_matrix(self):
        """ compute the projection and view matrices """
        glUseProgram(self.shader)

        self.projMatrix = glm.ortho(self.min_x, self.max_x, self.min_y, self.max_y, -5.0, 15.0)
        projLoc = glGetUniformLocation(self.shader, "projection")
        glUniformMatrix4fv(projLoc, 1, GL_FALSE, self.projMatrix)

        #self.viewMatrix = glm.ortho(self.min_x, self.max_x, self.min_y, self.max_y, -5.0, 15.0)
        viewLoc = glGetUniformLocation(self.shader, "view")
        glUniformMatrix4fv(viewLoc, 1, GL_FALSE, self.viewMatrix)

    def compute_transf_matrix_triangle(self):
        """ compute the model matrix for the triangle """

        
        #print(self.ty) 
        # code needed here
        self.modelMatrix_triangle = glm.scale(np.identity(4, np.float32), self.scale, self.scale, self.scale)

        self.modelMatrix_triangle = glm.rotate(self.modelMatrix_triangle, self.angle, 0, 0, 1.0)
        #self.modelMatrix_triangle = glm.rotate(self.modelMatrix_triangle, self.angle, 0, 0, 1.0)
        #self.modelMatrix_triangle = glm.scale(self.modelMatrix_triangle, 1, 1, 1)
        #self.modelMatrix_triangle = np.identity(4, np.float32)
        self.modelMatrix_triangle = glm.translate(self.modelMatrix_triangle, self.tx, self.ty, self.tz)

        viewLoc = glGetUniformLocation(self.shader, "model")
        glUniformMatrix4fv(viewLoc, 1, GL_FALSE, self.modelMatrix_triangle)

    def compute_transf_matrix_square(self):
        """ compute the model matrix to the square """

        # code needed here
        pass

    def process_events(self, keys):
        """ process keys that are being pressed and perform some actions """
        if keys[pg.K_UP]:
            self.ty += 0.05
            self.angle = 0
            if self.ty > self.max_y: # what is this code for? Answer: to not go out of bounds
                self.ty = self.min_y
        if keys[pg.K_DOWN]:
            self.ty -= 0.05
            self.angle = 180
            if self.ty < self.min_y: 
                self.ty = self.max_y
        if keys[pg.K_LEFT]:
            self.tx -= 0.05
            self.angle = 90
            if self.tx < self.min_x: 
                self.tx = self.max_x
        if keys[pg.K_RIGHT]:
            self.tx += 0.05
            self.angle = -90
            if self.tx > self.max_x: 
                self.tx = self.min_x

        
        
    def check_collisions(self):
        pass


    def animate(self):
        pass




# MAIN stuff

mygl = VCHelper()

pg.init()
windowSize = (800, 800)
pg.display.set_mode(windowSize, DOUBLEBUF | OPENGL | RESIZABLE)

glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glDisable(GL_LIGHTING)


mygl.initShaders()
mygl.initVertexBuffer()

while True:
    dt = mygl.clock.tick(60) # this ensures that this runs at 60 frames per second (ask why)
    mygl.process_events(pg.key.get_pressed())  # checking already pressed keys

    # simple check of colisions (needed ahead in the guide)
    mygl.check_collisions()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

    # simple animations
    mygl.animate()

    mygl.render()


