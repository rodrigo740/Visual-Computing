from panda3d.core import loadPrcFile
loadPrcFile("config/conf.prc")

from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath

class MyGame(ShowBase):
    def __init__(self):
        super().__init__()

        #self.disable_mouse()
        self.empty = NodePath("empty")

        self.cube = self.loader.loadModel("models/box")
        self.cube.setPos(0, 4 ,0)
        self.cube.reparentTo(self.empty)

        self.panda = self.loader.loadModel("models/panda")
        self.panda.setPos(-2, 10, 0)
        self.panda.setScale(0.2, 0.2, 0.2)
        self.panda.reparentTo(self.cube)

        self.empty.reparentTo(self.render)

        self.x = 0
        self.y = 4
        self.speed = 0.02

        self.taskMgr.add(self.update, "update")

    def update(self, task):
        dt = globalClock.getDt()
        self.cube.setPos(self.x, self.y, 0,)
        self.x += self.speed * dt
        self.y += self.speed * dt

        return task.cont



game = MyGame()
game.run()