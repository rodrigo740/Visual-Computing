from panda3d.core import loadPrcFile, PointLight, AmbientLight, NodePath
loadPrcFile("config/conf.prc")

from direct.showbase.ShowBase import ShowBase
from direct.filter.CommonFilters import CommonFilters
from direct.gui.DirectGui import *

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
        self.cam.lookAt(320,220,0)

        self.scaleZ = 30

        self.m = NodePath("m")

        self.a = 1/90

        self.floor = self.loader.loadModel("my-models/floor")
        self.floor.setPos(0, 0, 0)
        self.floor.setScale(100)
        self.floor.reparentTo(self.render)

        self.alight = AmbientLight("alight")
        self.alight.setColor((0.6, 0.6, 0.6, 1))
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

        self.disableICMP = False
        self.disableTCP = False
        self.disableUDP = False

        self.b3 = DirectCheckButton(text = "Pause" , scale=.08, command=self.b3Press, pos=(1.5, 0.5, 0.8))
        self.b4 = DirectCheckButton(text = "Shadows ON" , scale=.08, command=self.b4Press, pos=(1.5, 0.5, 0.5))
        self.b6 = DirectCheckButton(text = "ICMP OFF" , scale=.08, command=self.b6Press, pos=(1.5, 0.5, 0.3))
        self.b7 = DirectCheckButton(text = "TCP OFF" , scale=.08, command=self.b7Press, pos=(1.5, 0.5, 0.1))
        self.b8 = DirectCheckButton(text = "UDP OFF" , scale=.08, command=self.b8Press, pos=(1.5, 0.5, -0.1))
        
        self.pressed3 = False
        self.pressed4 = False
        self.pressed5 = False

        filters = CommonFilters(self.win, self.cam)     # halo effect
        filters.setBloom(size="medium")                 # halo effect


        
        

        self.taskMgr.add(self.move_pkt, "move-pkt")

    def b3Press(self, status):
        if self.pressed3:
            self.pressed3 = False
            self.taskMgr.add(self.move_pkt, "move-pkt")
            self.b3.setText("Pause")
        else:
            self.taskMgr.remove("move-pkt")
            self.pressed3 = True
            self.b3.setText("Resume")

    def b4Press(self, status):
        if self.pressed4:
            self.alight.setColor((0.6, 0.6, 0.6, 1))
            self.pressed4 = False
            self.render.setShaderOff()
            self.b4.setText("Shadows ON")
        else:
            self.alight.setColor((0.04, 0.04, 0.04, 1))
            self.pressed4 = True
            self.render.setShaderAuto()
            self.b4.setText("Shadows OFF")
    
    def b6Press(self, status):
        if self.disableICMP:
            self.disableICMP = False
            self.b6.setText("ICMP ON")
        else:
            self.disableICMP = True
            self.b6.setText("ICMP OFF")
    
    def b7Press(self, status):
        if self.disableTCP:
            self.disableTCP = False
            self.b7.setText("TCP ON")
        else:
            self.disableTCP = True
            self.b7.setText("TCP OFF")
    
    def b8Press(self, status):
        if self.disableUDP:
            self.disableUDP = False
            self.b8.setText("UDP ON")
        else:
            self.disableUDP = True
            self.b8.setText("UDP OFF")

    
    """
    In general, setPos() means “teleport the object here” and setFluidPos() means “slide the object here, testing for collisions along the way”.
    """
    def move_pkt(self, task):
        for pkt in self.pkts:
            if self.a >= pkt.timeStart:
                newPos = pkt.nextPos()
                if newPos != None:
                    if pkt.protocol == "icmp":
                        if self.disableICMP:
                            pkt.plnp.removeNode()
                        else:
                            pkt.lightModel.reparentTo(self.render)
                            pkt.lightModel.setFluidPos(newPos[0], newPos[1], self.scaleZ/2)
                    elif pkt.protocol == "tcp":
                        if self.disableTCP:
                            pkt.plnp.removeNode()
                        else:
                            pkt.lightModel.reparentTo(self.render)
                            pkt.lightModel.setFluidPos(newPos[0], newPos[1], self.scaleZ/2)

                    elif pkt.protocol == "udp":
                        if self.disableUDP:
                            pkt.plnp.removeNode()
                        else:
                            pkt.lightModel.reparentTo(self.render)
                            pkt.lightModel.setFluidPos(newPos[0], newPos[1], self.scaleZ/2)

                else:
                    pkt.lightModel.removeNode()
                    pkt.plnp.removeNode()
                    self.pkts.remove(pkt)
        if self.pkts == []:
            exit(0)

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

                if "PC" in aux[0]:
                    model = self.loader.loadModel("my-models/laptop_model/scene.gltf")
                    center = (x + w, y + h, 0)
                    model.setScale(3, 3, 3)

                elif "SW" in aux[0] or "R" in aux[0]:
                    model = self.loader.loadModel("my-models/router_model/scene.gltf")
                    center = (x + w/2, y + h, 0)
                    model.setScale(0.3)

                else:
                    model = self.loader.loadModel("models/box")   
                    center = (x + w/2, y + h/2, 0)
                    model.setScale(w, h, scaleZ)

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
                if k == id:
                    for (src, dst, time, delay, pc_id, pid, protocol) in self.ips[k]:
                        if self.dict[k] == src:
                            start = p1
                            end = p2
                        else:
                            start = p2
                            end = p1

                        light_model = self.loader.loadModel("models/misc/sphere")
                        light_model.setScale(6)

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

                        plnp = light_model.attachNewNode(plight)
                        self.floor.setLight(plnp)
                        self.m.setLight(plnp)

                        pkt = packet.Pkt((start, end), light_model, plnp, 1.5, float(time), protocol)
                        self.pkts.append(pkt)
            self.pktZ = self.pkts[0]


def main():
    coords, paths = parser.parseXML("utils/diagram.xml")
    ips = reader.getIPs()
    game = MyGame(coords, paths, ips)
    game.run()

if __name__ == "__main__":
    main()
