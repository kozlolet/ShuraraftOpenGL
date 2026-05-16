from src.scenes.play_scene.player import Player
from pyglet.window import key
from src.scenes.play_scene.world import World
from src.ui.ui_manager import UIManager
from src.ui.screens.in_game import InGame
from src.ui.screens.pause import Pause


class PlayScene:
    def __init__(self, game):
        self.game = game
        self.ctx = game.ctx
        self.keys = game.keys
        self.window = game.window

        self.player = Player(self)
        self.world = World(self)

        self.ui = UIManager(self)
        self.ui.register("in_game", InGame(self.ui))
        self.ui.register("pause", Pause(self.ui))
        self.ui.open("in_game")

        self.mouse_rotate = True

    def mouse_motion(self, x, y, dx, dy):
        self.ui.mouse_motion(x, y, dx, dy)

        if self.mouse_rotate:
            self.player.mouse_motion(x, y, dx, dy)

    def mouse_press(self, x, y, button, modifiers):
        self.player.mouse_press(x, y, button, modifiers)

    def key_release(self, symbol, modifiers):
        self.player.update_keys_release(symbol, modifiers)

    def key_press(self, symbol, modifiers):
        if self.ui.on_key_press(symbol, modifiers):
            return

        if symbol == key.Q:
            if self.mouse_rotate:
                self.ui.open("pause")
                self.window.set_exclusive_mouse(False)
                self.mouse_rotate = False
            else:
                self.ui.close("pause")
                self.window.set_exclusive_mouse(True)
                self.mouse_rotate = True

    def update(self, dt):
        # self.key_handle()
        self.world.update()
        self.player.update(dt)

    def draw(self):
        self.ctx.clear(0.1, 0.2, 0.3)
        self.world.draw()
        self.ui.draw()
