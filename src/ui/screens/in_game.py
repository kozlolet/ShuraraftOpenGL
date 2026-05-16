from pyglet.window import key
# from src.ui.objects import Rect
import pyglet


class InGame:
    def __init__(self, ui_manager):
        self.ui_manager = ui_manager
        self.visible = True
        self.blocks_game_input = False
        self.render = ui_manager.render

    def init_elements(self):
        center = self.ui_manager.get_center

        width, height = 50, 5
        x, y = center(width, height)
        self.cross_line1 = pyglet.shapes.Rectangle(
            x=x,
            y=y,
            width=width,
            height=height,
            color=(255, 255, 255)
        )

        width, height = 5, 50
        x, y = center(width, height)
        self.cross_line2 = pyglet.shapes.Rectangle(
            x=x,
            y=y,
            width=width,
            height=height,
            color=(255, 255, 255)
        )

    def on_open(self):
        self.init_elements()

    def on_close(self):
        pass

    def mouse_motion(self, x, y, dx, dy):
        pass

    def update(self, dt):
        pass

    def draw(self):
        if self.visible:
            self.cross_line1.draw()
            self.cross_line2.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.TAB:
            print("TAB pressed in HUD")
            return True
        return False
