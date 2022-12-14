from panda3d.core import loadPrcFile, PointLight, AmbientLight
loadPrcFile("config/conf.prc")

from direct.showbase.ShowBase import ShowBase
from math import sin, cos, pi
import utils.xml_parser as parser
import sys

scale = 50

class MyGame(ShowBase):
    def __init__(self, coords):
        super().__init__()
        self.accept("escape",sys.exit)

        self.set_background_color(0, 0, 0, 1)
        self.cam.setPos(100, -100, 100)
        #self.cam.setHpr(0, 90, 0)
        self.camLens.setFov(95)

        alight = AmbientLight("alight")
        alight.setColor((1, 1, 1, 1))
        alnp = self.render.attachNewNode(alight)
        
        print(coords)

        for (x, y, w, h) in coords:
            if float(x) > 10:
                model = self.loader.loadModel("models/box")
                model.setPos(float(y), float(x) , 0)
                model.setScale(scale)
                model.reparentTo(self.render)
                model.setLight(alnp)

        self.lightX = 0
        self.lightSpeed = 2

        self.light_model = self.loader.loadModel("models/misc/sphere")
        #self.light_model.setScale(scale)
        self.light_model.setPos(4, 0, 0)
        self.light_model.reparentTo(self.render)

        plight = PointLight("plight")
        plight.setColor((1, 0, 0, 1))
        
        plight = PointLight("plight")
        plight.setColor((1, 1, 1, 1))
        self.plnp = self.light_model.attachNewNode(plight)

        self.taskMgr.add(self.move_light, "move-light")

    def move_light(self, task):
        ft = globalClock.getFrameTime()
        self.light_model.setPos(cos(ft)*4, sin(ft)*4, 0)

        return task.cont




def main():
    coords = parser.parseXML("utils/diagram.xml")
    game = MyGame(coords)
    game.run()

if __name__ == "__main__":
    main()

        

