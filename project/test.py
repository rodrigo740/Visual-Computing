from panda3d.core import loadPrcFile, PointLight, AmbientLight
loadPrcFile("config/conf.prc")

from direct.showbase.ShowBase import ShowBase
from math import sin, cos, pi
import utils.xml_parser as parser
import sys

scale = 50

class Pkt():
    def __init__(self, path, lightModel, plnp):
        self.path = path
        self.lightModel = lightModel
        self.plnp = plnp
        self.currPos = path[0]
        self.i = 1

    def nextPos(self):
        self.currPos = (self.currPos[0]+self.i, self.currPos[1]+self.i)
        if (self.currPos[0] > self.path[1][0]) or (self.currPos[1] > self.path[1][1]):
            self.i = -1
        return self.currPos
        

class MyGame(ShowBase):
    def __init__(self, coords, paths):
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
        # generate figs
        for (x, y, w, h) in coords:
            if float(x) > 10:
                model = self.loader.loadModel("models/box")
                model.setPos(float(y), float(x) , 0)
                model.setScale(scale)
                model.reparentTo(self.render)
                model.setLight(alnp)

        self.lightX = 0
        self.lightSpeed = 2
        self.pkts = []

        for ((x1, y1), (x2, y2)) in paths:
            x1 =float(x1)
            y1 =float(y1)

            x2 =float(x2)
            y2 =float(y2)

            l1 = self.loader.loadModel("models/misc/sphere")
            #self.l1.setScale(scale)
            l1.setPos(x1, y1, 0)
            l1.reparentTo(self.render)

            p1 = PointLight("p1")
            p1.setColor((1, 0, 0, 1))
            
            plnp = l1.attachNewNode(p1)

            l2 = self.loader.loadModel("models/misc/sphere")
            #self.l2.setScale(scale)
            l2.setPos(x2, y2, 0)
            l2.reparentTo(self.render)

            p2 = PointLight("p2")
            p2.setColor((1, 0, 0, 1))
            
            plnp = l2.attachNewNode(p2)


        # generate pkts
        for ((x1, y1), (x2, y2)) in paths:
            x1 =float(x1)
            y1 =float(y1)

            x2 =float(x2)
            y2 =float(y2)

            light_model = self.loader.loadModel("models/misc/sphere")
            #self.light_model.setScale(scale)
            light_model.setPos(x1, y1, 0)
            light_model.reparentTo(self.render)

            plight = PointLight("plight")
            plight.setColor((1, 1, 1, 1))
            plnp = light_model.attachNewNode(plight)

            pkt = Pkt(((x1, y1), (x2, y2)), light_model, plnp)
            self.pkts.append(pkt)

        

        #self.taskMgr.add(self.move_light, "move-light")
        self.taskMgr.add(self.move_pkt, "move-pkt")
    """
    def move_light(self, task):
        ft = globalClock.getFrameTime()
        self.light_model.setPos(cos(ft)*4, sin(ft)*4, 0)

        return task.cont
    """
    
    def move_pkt(self, task):
        ft = globalClock.getFrameTime()
        for pkt in self.pkts:
            newPos = pkt.nextPos()
            pkt.lightModel.setPos(newPos[0], newPos[1], 0)

        return task.cont




def main():
    coords, paths = parser.parseXML("utils/diagram.xml")
    game = MyGame(coords, paths)
    game.run()

if __name__ == "__main__":
    main()

        

