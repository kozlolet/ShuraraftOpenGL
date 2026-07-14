from src.scenes.play_scene.player.player import Player
from pyglet.window import key
from src.scenes.play_scene.world.world import World
from src.ui.ui_manager import UIManager
from src.ui.screens.in_game import InGame
from src.ui.screens.pause import Pause
from src.render.sky.sky_render import SkyRender


class PlayScene:
    def __init__(self, game, world_name):
        self.game = game
        self.ctx = game.ctx
        self.keys = game.keys
        self.window = game.window

        self.world_name = world_name
        self.world = World(self)
        self.player = Player(self)
        self.sky = SkyRender(self.ctx, bottom_color=(1.0, 0.8, 0.8), top_color=(0.2, 0.5, 1.0))

        self.ui = UIManager(self)
        self.ui.register("in_game", InGame(self.ui))
        self.ui.register("pause", Pause(self.ui))
        self.ui.open("in_game")

        self.paused = False
        self.window.set_exclusive_mouse(True)

    def mouse_motion(self, x, y, dx, dy):
        self.ui.mouse_motion(x, y, dx, dy)

        if not self.paused:
            self.player.mouse_motion(x, y, dx, dy)

    def mouse_press(self, x, y, button, modifiers):
        if not self.paused:
            self.player.mouse_press(x, y, button, modifiers)

    def mouse_release(self, x, y, button, modifiers):
        if self.paused:
            self.ui.mouse_release(x, y, button, modifiers)

    def key_release(self, symbol, modifiers):
        self.player.update_keys_release(symbol, modifiers)

    def key_press(self, symbol, modifiers):
        if self.ui.on_key_press(symbol, modifiers):
            return

        if symbol == key.Q:
            if not self.paused:
                self.set_paused(True)
            else:
                self.set_paused(False)

    def set_paused(self, paused: bool):
        self.paused = paused
        self.window.set_exclusive_mouse(not paused)

        if paused:
            self.ui.open("pause")
        else:
            self.ui.close("pause")

    def update(self, dt):
        self.world.update()
        self.player.update(dt)

    def draw(self):
        self.ctx.clear(0.0, 0.0, 0.0)
        self.sky.draw()
        self.world.draw()
        self.ui.draw()
