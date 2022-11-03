import random

from panda3d.core import loadPrcFile
from panda3d.core import *
loadPrcFile("config/config.prc")
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import os, sys
import math

class MyGame(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # Get the location of the 'py' file I'm running:
        self.mydir = os.path.abspath(sys.path[0])
        # convert to panda's specific notation
        self.mydir = Filename.fromOsSpecific(self.mydir).getFullpath()
        
        # models:
        # Skull
        self.skullModel = self.loader.loadModel(self.mydir + "/skull.obj")
        self.skullModel.setPos(0, 0, -5)
        self.skullModel.reparentTo(self.render)
        self.skullModel.setScale(0.35,0.35,0.35)
        # Panda
        self.pandaModel = self.loader.loadModel("models/panda")
        self.pandaModel.setPos(0, 0, 30)
        self.pandaModel.setP(90)
        self.pandaModel.setScale(.6,.6,.6)
        self.pandaModel.reparentTo(self.skullModel)
        
        # camera pos and controls
        self.disableMouse()
        self.camera.setPos(0, -30, 0)
        self.cameraRadius = 30.0
        
        # light sources
        self.plight1 = PointLight('plight')
        self.plight1.setColor((1, 1, 1, 1))
        self.plnp1 = self.render.attachNewNode(self.plight1)
        self.plnp1.setPos(0, -10, 10)
        self.render.setLight(self.plnp1)

        self.alight = AmbientLight('alight')
        self.alight.setColor((0.2, 0.2, 0.2, 1))
        self.alnp = self.render.attachNewNode(self.alight)
        self.render.setLight(self.alnp)

        self.plight2 = PointLight('plight')
        self.plight2.setColor((0, 0, 1, 1))
        self.plnp2 = self.render.attachNewNode(self.plight2)
        self.plnp2.setPos(0, 30, 10)
        self.render.setLight(self.plnp2)

        self.alight2 = AmbientLight('alight')
        self.alight2.setColor((1, 0, 0, 1))
        self.alnp2 = self.render.attachNewNode(self.alight2)
        self.pandaModel.setLight(self.alnp2)

        # tasks
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        self.taskMgr.add(self.spinPandaTask, "spinPandaTask")
        self.taskMgr.add(self.moveTask, "moveTask")

    def spinCameraTask(self, task):
        angleDegrees = task.time * 20.0
        angleRadians = angleDegrees * (math.pi / 180.0)
        self.camera.setPos(self.cameraRadius * math.sin(angleRadians), -self.cameraRadius * math.cos(angleRadians),0)
        self.camera.lookAt(0.0, 0.0, 0.0)

        return Task.cont

    def spinPandaTask(self, task):
        angleDegrees = task.time * 40.0
        angleRadians = angleDegrees * (math.pi / 180.0)
        self.pandaModel.setPos(10 * math.sin(angleRadians), -10 * math.cos(angleRadians),30)
        self.pandaModel.setH(angleDegrees)

        return Task.cont

    def moveTask(self, task):
        isDown = base.mouseWatcherNode.isButtonDown
        if isDown(KeyboardButton.asciiKey("+")):
            self.cameraRadius += 1
        if isDown(KeyboardButton.asciiKey("-")):
            self.cameraRadius -= 1
        
        return Task.cont


# create an object for the game and run it
game = MyGame()
game.run()