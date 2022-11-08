from panda3d.core import loadPrcFile
loadPrcFile("config/conf.prc")

from direct.showbase.ShowBase import ShowBase

# callback function to update the keyMap
def updateKeyMap(key, state):
    keyMap[key] = state

class MyGame(ShowBase):
    def __init__(self):
        super().__init__()

        self.disable_mouse()

        # mouse left button
        self.accept("mouse1", self.mouse_click)
        self.accept("mouse1-up", self.mouse_click)

        # mouse middle button
        self.accept("mouse2", self.mouse_click)
        self.accept("mouse2-up", self.mouse_click)

        # mouse right button
        self.accept("mouse3", self.mouse_click)
        self.accept("mouse3-up", self.mouse_click)


        self.taskMgr.add(self.update, "update")

    def mouse_click(self):
        pass
        #md1 = self.win.getPointer(0)
        #print(md1.getX(), md1.getY()) # from  x: 0 to 1200 and y: 0 to 720

        #md2 = self.mouseWatcherNode.getMouse()
        #print(md2.getX(), md2.getY()) # from  x: -1 to 1 and y: -1 to 1

    def update(self, task):
        #md = self.win.getPointer(0)
        #print(md.getX(), md.getY())

        if self.mouseWatcherNode.hasMouse():
            x = self.mouseWatcherNode.getMouseX()
            y = self.mouseWatcherNode.getMouseY()
            print(x, y)

        return task.cont



game = MyGame()
game.run()