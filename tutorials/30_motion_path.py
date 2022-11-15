from panda3d.core import loadPrcFile
loadPrcFile("config/conf.prc")

from direct.showbase.ShowBase import ShowBase
from direct.directutil import Mopath
from direct.interval.MopathInterval import *
from direct.filter.CommonFilters import CommonFilters

class MyGame(ShowBase):
    def __init__(self):
        super().__init__()
        self.set_background_color(0, 0, 0, 1)
        self.cam.setPos(0, -80, 0)

        self.light_model = self.loader.loadModel("models/misc/sphere")
        self.light_model.setScale(0.5)
        self.light_model.reparentTo(self.render)

        my_curve = Mopath.Mopath()
        my_curve.loadFile("my-models/curvey")

        my_interval = MopathInterval(my_curve, self.light_model, name="my-path", duration=2)
        #my_interval.start()
        my_interval.loop()

        filters = CommonFilters(self.win, self.cam)
        filters.setBloom(size="large")

        print(my_curve.xyzNurbsCurve.getNumKnots())
        print(my_curve.xyzNurbsCurve.getOrder())
        print(my_curve.xyzNurbsCurve.getNumCvs())
        print(my_curve.xyzNurbsCurve.getKnots())
        

game = MyGame()
game.run()