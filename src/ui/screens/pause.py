from pyglet.window import key
import pyglet
from src.ui.objects import Rect


class Pause:
    def __init__(self, ui_manager):
        self.ui_manager = ui_manager
        self.visible = True
        self.blocks_game_input = False
        self.render = ui_manager.render

    def init_elements(self):
        width = 0.6
        height = 0.6
        center_x, center_y = self.ui_manager.get_center(width, height)
        self.main_rect = Rect(screen=self,
                         x_ratio=center_x,
                         y_ratio=center_y,
                         width_ratio=width,
                         height_ratio=height,
                         color=(50, 50, 50, 0))

        width = 0.5
        height = 0.1
        center_x, center_y = self.ui_manager.get_center(width, height)
        self.b_continue = Rect(screen=self,
                               x_ratio=center_x,
                               y_ratio=0.7,
                               width_ratio=width,
                               height_ratio=height,
                               color=(100, 100, 100, 0))

    def on_open(self):
        self.init_elements()

    def on_close(self):
        pass

    def mouse_motion(self, x, y, dx, dy):
        if self.b_continue.mouse_in(x, y):
            self.b_continue.color = (150, 150, 150, 0)
        else:
            self.b_continue.color = (100, 100, 100, 0)

    def update(self, dt):
        pass

    def draw(self):
        if self.visible:
            self.b_continue.draw()
            self.main_rect.draw()


    def on_key_press(self, symbol, modifiers):
        if symbol == key.TAB:
            print("TAB pressed in pause")
            return True
        return False
