from panda3d.core import loadPrcFile
loadPrcFile("config/conf.prc")

from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath

class MyGame(ShowBase):
    def __init__(self):
        super().__init__()

        #self.disable_mouse()
        empty = NodePath("empty")

        cube = self.loader.loadModel("models/box")
        cube.setPos(0, 4 ,0)
        cube.reparentTo(empty)

        panda = self.loader.loadModel("models/panda")
        panda.setPos(-2, 10, 0)
        panda.setScale(0.2, 0.2, 0.2)
        panda.reparentTo(cube)

        empty.reparentTo(self.render)



game = MyGame()
game.run()