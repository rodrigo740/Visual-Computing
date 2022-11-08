from panda3d.core import loadPrcFile
loadPrcFile("config/conf.prc")

from direct.showbase.ShowBase import ShowBase


keyMap = {
    "up": False,
    "down": False,
    "left": False,
    "right": False,
    "rotate": False
}

# callback function to update the keyMap
def updateKeyMap(key, state):
    keyMap[key] = state

class MyGame(ShowBase):
    def __init__(self):
        super().__init__()

        #self.disable_mouse()

        self.cam.setPos(0, -10, 0)

        self.jack = self.loader.loadModel("models/jack")
        self.jack.setHpr(0, 180, 180)
        self.jack.reparentTo(self.render)

        self.accept("arrow_left", updateKeyMap, ["left", True])
        self.accept("arrow_left-up", updateKeyMap, ["left", False])

        self.accept("arrow_right", updateKeyMap, ["right", True])
        self.accept("arrow_right-up", updateKeyMap, ["right", False])

        self.accept("arrow_up", updateKeyMap, ["up", True])
        self.accept("arrow_up-up", updateKeyMap, ["up", False])

        self.accept("arrow_down", updateKeyMap, ["down", True])
        self.accept("arrow_down-up", updateKeyMap, ["down", False])

        self.accept("space", updateKeyMap, ["rotate", True])
        self.accept("space-up", updateKeyMap, ["rotate", False])

        self.speed = 4
        self.angle = 0

        self.taskMgr.add(self.update, "update")

    def update(self, task):
        dt = globalClock.getDt()

        pos = self.jack.getPos()

        if keyMap["left"]:
            pos.x -= self.speed * dt
        if keyMap["right"]:
            pos.x += self.speed * dt
        if keyMap["up"]:
            pos.z += self.speed * dt
        if keyMap["down"]:
            pos.z -= self.speed * dt
        if keyMap["rotate"]:
            self.angle += 1
            self.jack.setH(self.angle)

        self.jack.setPos(pos)


        return task.cont



game = MyGame()
game.run()