from OpenGL.GL import *
import pygame as pg
from pygame.locals import *

pg.init()
windowsize = (1250, 1250)
pg.display.set_mode(windowsize, DOUBLEBUF | OPENGL | RESIZABLE)

glClearColor(0.0, 1.0, 0.0, 1.0)

while True:
    glClear(GL_COLOR_BUFFER_BIT)
    pg.display.flip()
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()