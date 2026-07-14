from src.ui.ui_manager import UIManager
from src.ui.screens.main_menu import MainMenu


class MainMenuScene:
    def __init__(self, game):
        self.game = game
        self.ctx = game.ctx
        self.keys = game.keys
        self.window = game.window

        self.window.set_exclusive_mouse(False)

        self.ui = UIManager(self)
        self.ui.register("main_menu", MainMenu(self.ui))
        self.ui.open("main_menu")

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