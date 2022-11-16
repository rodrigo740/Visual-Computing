from panda3d.core import loadPrcFile
loadPrcFile("config/conf.prc")

from direct.showbase.ShowBase import ShowBase
import xml.etree.ElementTree as ET
from math import sin, cos, pi

class MyGame(ShowBase):
    def __init__(self, coords):
        super().__init__()
        self.set_background_color(0, 0, 0, 1)
        self.cam.setPos(0, -100, 20)
        #self.cam.setHpr(0, 0, 10)
        print(coords)

        for (x, y, w, h) in coords:
            model = self.loader.loadModel("models/box")
            model.setPos(float(y), float(x) , 0)
            model.reparentTo(self.render)

        #self.model = self.loader.loadModel("assets/OBJ-format/light_curved.obj")
        #self.model.reparentTo(self.render)
        #self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(0, angleDegrees, angleDegrees)
        return task.cont


def parseXML(xmlfile):
  
    # create element tree object
    tree = ET.parse(xmlfile)
  
    # get root element
    root = tree.getroot()

    # create empty list for news items
    coords = []
  
    # iterate news items
    for _ in root:
        for item in _.findall('mxCell'):
            #print(item.tag, item.attrib)
            for figure in item.findall('mxGeometry'):
                x = figure.get('x')
                y = figure.get('y')
                w = figure.get('width')
                h = figure.get('height')
                if (x != None) and (y != None):
                    #print(x, y)
                    coords.append((x,y,w,h))
        #for item in _:
        #    print(item.tag, item.attrib)
    return coords

def main():
    coords = parseXML("diagram.xml")
    game = MyGame(coords)
    game.run()

if __name__ == "__main__":
    main()

        

