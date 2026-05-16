from src.render.ui_renderer import UIRenderer


class UIManager:
    def __init__(self, scene):
        self.scene = scene
        self.ctx = scene.ctx
        self.window = scene.window

        self.screens = {}
        self.active_screens = []

        # self.start_window_width = scene.game.start_window_width
        # self.start_window_height = scene.game.start_window_height
        self.render = UIRenderer(self.ctx, self.window)

    def reload_uv(self):
        for screen in self.active_screens:
            screen.on_close()
            screen.on_open()

    def get_center(self, width=0, height=0):
        center_x = (self.window.width - width) / 2
        center_y = (self.window.height - height) / 2
        return center_x, center_y

    def in_ratio(self, pixels_x, pixels_y):
        return pixels_x / self.window.width, pixels_y / self.window.height

    def mouse_motion(self, x, y, dx, dy):
        last_screen = self.active_screens[-1]
        last_screen.mouse_motion(x, y, dx, dy)

    def register(self, name, screen):
        self.screens[name] = screen

    def open(self, name):
        screen = self.screens[name]
        if screen not in self.active_screens:
            self.active_screens.append(screen)
            screen.on_open()

    def close(self, name):
        screen = self.screens[name]
        if screen in self.active_screens:
            self.active_screens.remove(screen)
            screen.on_close()

    def update(self, dt):
        for screen in self.active_screens:
            screen.update(dt)

    def draw(self):
        for screen in self.active_screens:
            screen.draw()

    def on_key_press(self, symbol, modifiers):
        for screen in reversed(self.active_screens):
            if screen.on_key_press(symbol, modifiers):
                return True
        return False
