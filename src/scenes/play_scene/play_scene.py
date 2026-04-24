from src.scenes.play_scene.player import Player
from pyglet.window import key
from src.scenes.play_scene.world import World


class PlayScene:
    def __init__(self, game):
        self.game = game
        self.ctx = game.ctx
        self.keys = game.keys
        self.window = game.window

        self.player = Player(self)
        self.world = World(self)

        self.mouse_rotate = True

    def mouse_handle(self, x, y, dx, dy):
        if self.mouse_rotate:
            self.player.mouse_handle(x, y, dx, dy)

    def keys_handle(self):
        # keys = self.keys
        pass

    def key_press_handle(self, symbol, modifiers):
        if symbol == key.Q:
            if self.mouse_rotate:
                self.window.set_exclusive_mouse(False)
                self.mouse_rotate = False
            else:
                self.window.set_exclusive_mouse(True)
                self.mouse_rotate = True

    def update(self, dt):
        self.keys_handle()
        self.world.update()
        self.player.update(dt)

    def draw(self):
        self.ctx.clear(0.1, 0.2, 0.3)
        self.world.draw()
