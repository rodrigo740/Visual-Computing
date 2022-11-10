from panda3d.core import loadPrcFile
loadPrcFile("config/conf.prc")

from direct.showbase.ShowBase import ShowBase
from panda3d.core import OrthographicLens

class MyGame(ShowBase):
    def __init__(self):
        super().__init__()

        self.set_background_color(0.1, 0.1, 0.1, 1)
        self.cam.setPos(0, -5, 0)

        self.cube1 = self.loader.loadModel("models/box")
        self.cube1.setPos(1, 0, 0)
        self.cube1.reparentTo(self.render)

        self.cube2 = self.loader.loadModel("models/box")
        self.cube2.setPos(-3, 8, 0)
        self.cube2.reparentTo(self.render)

        lens = OrthographicLens()
        lens.setFilmSize(16, 9)
        lens.setNearFar(-58, 58)
        self.cam.node().setLens(lens)
        

game = MyGame()
game.run()