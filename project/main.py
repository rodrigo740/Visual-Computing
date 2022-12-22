from panda3d.core import loadPrcFile, PointLight, AmbientLight
loadPrcFile("config/conf.prc")

from direct.showbase.ShowBase import ShowBase
from direct.filter.CommonFilters import CommonFilters
from math import sin, cos, pi, dist
import utils.xml_parser as parser
import utils.Pkt as packet
import sys


class MyGame(ShowBase):
    def __init__(self, coords, paths):
        super().__init__()
        self.accept("escape",sys.exit)

        self.set_background_color(0, 0, 0, 1)
        self.cam.setPos(320, 220, 2000)
        #self.cam.setHpr(0, 90, 0)
        #self.camLens.setFov(95)
        self.cam.lookAt(320,220,0)

        self.scaleZ = 30

        self.alight = AmbientLight("alight")
        self.alight.setColor((1, 1, 1, 1))
        self.alnp = self.render.attachNewNode(self.alight)
        
        self.models = self.gen_figs(coords, self.scaleZ)

        self.lightX = 0
        self.lightSpeed = 2
        self.pkts = []

        self.count = 1/75
        
        for ((x1, y1), (x2, y2)) in paths:
            x1 =float(x1)+60
            y1 =float(y1)+30

            x2 =float(x2)+60
            y2 =float(y2)+30

            #print((x1,y1))
            #print((x2,y2))
            """
            m1 = self.loader.loadModel("models/box")
            center = (x1, y1, 0)
            m1.setPos(center)
            m1.setScale(25, 25, 0)
            m1.reparentTo(self.render)
            m1.setLight(self.alnp)

            m2 = self.loader.loadModel("models/box")
            center = (x2, y2, 0)
            m2.setPos(center)
            m2.setScale(25, 25, 0)
            m2.reparentTo(self.render)
            m2.setLight(self.alnp)
            """
            
            l1 = self.loader.loadModel("models/misc/sphere")
            l1.setColor(1,0,0)
            #self.l1.setScale(scale)
            l1.setPos(x1, y1, self.scaleZ/2)
            l1.reparentTo(self.render)

            p1 = PointLight("p1")
            p1.setColor((1, 0, 0, 1))
            
            plnp = l1.attachNewNode(p1)


            l2 = self.loader.loadModel("models/misc/sphere")
            l2.setColor(1,0,0)
            #self.l2.setScale(scale)
            l2.setPos(x2, y2, self.scaleZ/2)
            l2.reparentTo(self.render)

            p2 = PointLight("p2")
            p2.setColor((1, 0, 0, 1))
            
            plnp = l2.attachNewNode(p2)
            
        t = 2

        filters = CommonFilters(self.win, self.cam)     # halo effect
        filters.setBloom(size="large")                  # halo effect
        
        # generate pkts
        for ((x1, y1), (x2, y2)) in paths:
            for _ in range(100):
                x1 =float(x1)+60
                y1 =float(y1)+30

                x2 =float(x2)+60
                y2 =float(y2)+30

                print((x1,y1))
                print((x2,y2))

                light_model = self.loader.loadModel("models/misc/sphere")
                light_model.setScale(15)
                light_model.reparentTo(self.render)
                light_model.setPos(x1, y1, self.scaleZ/2)

                plight = PointLight("plight")
                plight.setColor((0, 1, 0, 1))
                plnp = light_model.attachNewNode(plight)

                pkt = packet.Pkt(((x1, y1), (x2, y2)), light_model, plnp, t)
                #t += 2
                #print("T: " + str(t))
                self.pkts.append(pkt)

        #self.taskMgr.add(self.move_light, "move-light")
        self.taskMgr.add(self.move_pkt, "move-pkt")
    
    def move_light(self, task):
        ft = globalClock.getFrameTime()
        self.cam.setPos(cos(ft)*4, sin(ft)*4, 0)

        return task.cont
    
    
    """
    In general, setPos() means “teleport the object here” and setFluidPos() means “slide the object here, testing for collisions along the way”.
    """
    def move_pkt(self, task):
        ft = globalClock.getFrameTime()
        #if self.count < 20/75:
        for pkt in self.pkts:
            newPos = pkt.nextPos()
            if newPos != None:
                pkt.lightModel.setFluidPos(newPos[0], newPos[1], self.scaleZ/2)

        #self.count += self.count
        #print(self.count)
        #if self.count >= 1:
        #    self.count = 1/75

        return task.cont


    def gen_figs(self, coords, scaleZ):
        models = []
        print(coords)
        # generate figs
        for (x, y, w, h) in coords:
            if float(x) > 10 and w != None and h != None:
                x = float(x)
                y = float(y)
                w = float(w)
                h = float(h)
                model = self.loader.loadModel("models/box")
                center = (x + w/2, y + h/2, 0)
                model.setScale(w, h, scaleZ)
                
                p = self.loader.loadModel("models/misc/sphere")
                p.setPos(center)
                p.reparentTo(self.render)
                
                model.setPos(center)
                model.reparentTo(self.render)
                model.setLight(self.alnp)
                models.append(model)

        return models

        



def main():
    coords, paths = parser.parseXML("utils/diagram.xml")
    game = MyGame(coords, paths)
    game.run()

if __name__ == "__main__":
    main()
