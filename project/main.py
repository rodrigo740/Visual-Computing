from panda3d.core import loadPrcFile, PointLight, AmbientLight, NodePath, loadPrcFileData
loadPrcFile("config/conf.prc")
#loadPrcFileData("", "gl-version 3 2")
from direct.showbase.ShowBase import ShowBase
from direct.filter.CommonFilters import CommonFilters
from direct.gui.DirectGui import *
from math import sin, cos, pi
import utils.xml_parser as parser
import utils.Pkt as packet
import utils.pcapReader as reader
import sys


class MyGame(ShowBase):
    def __init__(self, coords, paths, ips):
        super().__init__()
        self.accept("escape",sys.exit)

        self.set_background_color(0, 0, 0, 1)
        self.cam.setPos(320, 220, 2000)
        #self.cam.setHpr(0, 90, 0)
        #self.camLens.setFov(95)
        self.cam.lookAt(320,220,0)

        self.scaleZ = 30

        self.m = NodePath("m")

        self.a = 1/90

        self.floor = self.loader.loadModel("my-models/floor")
        self.floor.setPos(0, 0, 0)
        self.floor.setScale(100)
        self.floor.reparentTo(self.render)

        self.alight = AmbientLight("alight")
        self.alight.setColor((0.04, 0.04, 0.04, 1))
        #self.alight.setColor((0, 0, 0, 1))
        self.alnp = self.render.attachNewNode(self.alight)

        self.floor.setLight(self.alnp)

        self.dict = {}
        
        self.models = self.gen_figs(coords, self.scaleZ)

        self.lightX = 0
        self.lightSpeed = 2
        self.pkts = []

        self.count = 1/75
        self.ips = ips
        self.paths = paths
        self.gen_pkts()

        #b = DirectButton(text=("Shadows", "click!", "rolling over", "disabled"), scale=.06, pos=(-1.5, 0.5, 0.5))
        v = [0]
        #b2 = DirectRadioButton(text='Shadows', variable=v, value=[1], scale=0.05, pos=(-1.5, 0.5, 0.4))

        #b3 = DirectCheckButton(text = "Shadows" , scale=.05, command=self.b3Press)
        
        """
        for ((x1, y1), (x2, y2)) in paths:
            x1 =float(x1)+60
            y1 =float(y1)+30

            x2 =float(x2)+60
            y2 =float(y2)+30
            
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
        """

        #filters = CommonFilters(self.win, self.cam)     # halo effect
        #filters.setBloom(size="large")                  # halo effect
        

        #self.taskMgr.add(self.move_light, "move-light")
        self.taskMgr.add(self.move_pkt, "move-pkt")
    
    def move_light(self, task):
        ft = globalClock.getFrameTime()
        self.cam.setPos(cos(ft)*4, sin(ft)*4, 0)

        return task.cont
    
    def b3Press(self, status):
        print("Pressed")

    
    """
    In general, setPos() means “teleport the object here” and setFluidPos() means “slide the object here, testing for collisions along the way”.
    """
    def move_pkt(self, task):
        #ft = globalClock.getFrameTime()
        #a = globalClock.getDt()
        #print(ft)
        #self.dt += self.dt
        #if ft >= 10:
        #    print("10 seconds has passed")
        #print(dt)
        #if self.count < 20/75:
        for pkt in self.pkts:
            #print(pkt.timeStart)
            if self.a >= pkt.timeStart:
            #if ft >= pkt.timeStart:
                newPos = pkt.nextPos()
                if newPos != None:
                    pkt.lightModel.reparentTo(self.render)

                    pkt.lightModel.setFluidPos(newPos[0], newPos[1], self.scaleZ/2)
                else:
                    pkt.lightModel.removeNode()
                    pkt.plnp.removeNode()
                    self.pkts.remove(pkt)
        self.a += 1/75
        #print(self.a)

        #self.count += self.count
        #print(self.count)
        #if self.count >= 1:
        #    self.count = 1/75

        return task.cont


    def gen_figs(self, coords, scaleZ):
        models = []
        # generate figs
        for (x, y, w, h, ip) in coords:
            if float(x) > 10 and w != None and h != None:
                x = float(x)
                y = float(y)
                w = float(w)
                h = float(h)
                
                aux = ip.split(" ")

                if len(aux) > 1:
                    self.dict[aux[0]] = aux[1]

                model = self.loader.loadModel("models/box")
                center = (x + w/2, y + h/2, 0)
                model.setScale(w, h, scaleZ)
                """
                p = self.loader.loadModel("models/misc/sphere")
                p.setPos(center)
                p.reparentTo(self.render)
                """
                model.setPos(center)
                model.reparentTo(self.m)
                model.setLight(self.alnp)
                models.append(model)

        self.m.reparentTo(self.render)
        return models

    def gen_pkts(self):
        # generate pkts
        for (id, (x1, y1), (x2, y2)) in self.paths:
            id = id.split(" ")[1]
            
            x1 =float(x1)+60
            y1 =float(y1)+30

            x2 =float(x2)+60
            y2 =float(y2)+30

            p1 = (x1,y1)
            p2 = (x2,y2)

            r = 0
            g = 0
            b = 0
            
            for k in self.ips:
                #print(k)
                if k == id:
                    for (src, dst, time, delay, pc_id, pid, protocol) in self.ips[k]:
                        #print("key: {}, src: {}, dst: {}, time: {}, delay: {}, pid: {}".format(k, src, dst, time, delay, pid))
                        #print(self.dict[k])
                        if self.dict[k] == src:
                            start = p1
                            end = p2
                        else:
                            start = p2
                            end = p1

                        light_model = self.loader.loadModel("models/misc/sphere")
                        light_model.setScale(15)
                        #light_model.reparentTo(self.render)
                        #light_model.setPos(start[0], start[1], self.scaleZ/2)

                        plight = PointLight("plight")

                        if protocol == "tcp":
                            r = 1
                            g = 0
                            b = 0
                        elif protocol == "udp":
                            r = 0
                            g = 1
                            b = 0
                        elif protocol == "icmp":
                            r = 0
                            g = 0
                            b = 1
                        else:
                            r = 0
                            g = 0
                            b = 0

                        plight.setColor((r, g, b, 1))
                        #plight.setShadowCaster(True, 10, 10)        # shadows

                        plnp = light_model.attachNewNode(plight)
                        self.floor.setLight(plnp)
                        self.m.setLight(plnp)

                        pkt = packet.Pkt((start, end), light_model, plnp, 1.5, float(time), protocol)
                        #t += 0.5
                        #print("T: " + str(t))
                        self.pkts.append(pkt)
                        
            self.render.setShaderAuto()                   # shadows
            
        
        """
        for mdl in self.models:
            for pkt in self.pkts:
                mdl.setLight(pkt.plnp)
        """


        """
        # generate pkts
        for ((x1, y1), (x2, y2)) in paths:
            for _ in range(1):
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
                print("T: " + str(t))
                self.pkts.append(pkt)
        """

        


def main():
    coords, paths = parser.parseXML("utils/ndg.xml")
    ips = reader.getIPs()
    game = MyGame(coords, paths, ips)
    game.run()

if __name__ == "__main__":
    main()
