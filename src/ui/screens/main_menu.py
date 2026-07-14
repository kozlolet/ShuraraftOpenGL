import pyglet
from src.ui.elements.button import Button


class MainMenu:
    def __init__(self, ui_manager):
        self.game = ui_manager.game
        self.ui_manager = ui_manager
        self.visible = True
        self.render = ui_manager.render
        self.elements = []

    def init_elements(self):
        center = self.ui_manager.get_center
        from_ratio = self.ui_manager.from_ratio

        def on_hover(button):
            button.color = (100, 100, 100)

        def on_click(button):
            self.game.change_scene("world_selection_scene")

        width, height = from_ratio(0.5, 0.08)
        _, offset_y = from_ratio(0, 0.05)
        x, y = center(width, height)
        self.elements.append(
            Button(
                x=x, y=y+offset_y,
                width=width, height=height,
                color=(60, 60, 60),
                text="играть", font_size=48,
                on_hover=on_hover,
                on_click=on_click
            )
        )

        def on_click(button):
            pyglet.app.exit()

        width, height = from_ratio(0.5, 0.08)
        _, offset_y = from_ratio(0, 0.05)
        x, y = center(width, height)
        self.elements.append(
            Button(
                x=x, y=y-offset_y,
                width=width, height=height,
                color=(60, 60, 60),
                text="выйти из игры", font_size=48,
                on_hover=on_hover,
                on_click=on_click
            )
        )

    def on_open(self):
        self.elements = []
        self.init_elements()

    def on_close(self):
        pass

    def mouse_motion(self, x, y, dx, dy):
        for element in self.elements:
            element.mouse_motion(x, y)

    def mouse_release(self, x, y, button, modifiers):
        for element in self.elements:
            element.mouse_release(x, y, button, modifiers)

    def update(self, dt):
        pass

    def draw(self):
        if not self.visible:
            return
        for element in self.elements:
            element.draw()

    def on_key_press(self, symbol, modifiers):
        pass