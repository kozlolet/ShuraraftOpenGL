from src.ui.ui_manager import UIManager
from src.ui.screens.world_selection import WorldSelection
from pathlib import Path
import os
import pyglet


class WorldSelectionScene:
    def __init__(self, game):
        self.game = game
        self.ctx = game.ctx
        self.keys = game.keys
        self.window = game.window

        self.src_path = Path(__file__).resolve().parent.parent.parent
        self.window.set_exclusive_mouse(False)

        self.worlds = []
        self.read_worlds()

        self.ui = UIManager(self)
        self.ui.register("world_selection", WorldSelection(self.ui, self.worlds))
        self.ui.open("world_selection")

    def read_worlds(self):
        for name in os.listdir(self.src_path / 'worlds'):
            image = pyglet.image.load(self.src_path / 'worlds' / name / 'logo.png')
            self.worlds.append({
                "name": name,
                "logo": image
            })

    def mouse_motion(self, x, y, dx, dy):
        self.ui.mouse_motion(x, y, dx, dy)

    def mouse_press(self, x, y, button, modifiers):
        pass

    def mouse_release(self, x, y, button, modifiers):
        self.ui.mouse_release(x, y, button, modifiers)

    def key_release(self, symbol, modifiers):
        pass

    def key_press(self, symbol, modifiers):
        pass

    def update(self, dt):
        pass

    def draw(self):
        self.ctx.clear(0.1, 0.2, 0.3)
        self.ui.draw()