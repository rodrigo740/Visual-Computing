from panda3d.core import loadPrcFile
loadPrcFile("config/conf.prc")

from direct.showbase.ShowBase import ShowBase


class MyGame(ShowBase):
    def __init__(self):
        super().__init__()

        self.set_background_color(0.1, 0.1, 0.1, 1)
        self.cam.setPos(0, -5, 0)

        self.jack = self.loader.loadModel("assets/texture_cards/Jack")
        self.jack.reparentTo(self.render)
        

game = MyGame()
game.run()