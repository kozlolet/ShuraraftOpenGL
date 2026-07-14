import pyglet
from src.ui.elements.button import Button
from src.ui.elements.image import Image


class WorldSelection:
    def __init__(self, ui_manager, worlds):
        self.game = ui_manager.game
        self.ui_manager = ui_manager
        self.visible = True
        self.render = ui_manager.render
        self.elements = []

        self.worlds = worlds

    def init_elements(self):
        center = self.ui_manager.get_center
        from_ratio = self.ui_manager.from_ratio
        window = self.ui_manager.window

        top = 100
        _, offset = from_ratio(0, 0.12)

        for i, world_data in enumerate(self.worlds):
            def on_hover(button):
                button.color = (100, 100, 100)
            def on_click(button):
                self.ui_manager.game.change_scene("play_scene", agrs=(button.data['world_name'],))

            left, a = from_ratio(0.2, 0.1)
            world_data['logo'].scale = 4
            self.elements.append(Image(
                image=world_data['logo'],
                x=left, y=window.height - a - top - offset * i,
                width=a, height=a,
            ))

            width, height = from_ratio(0.5, 0.1)
            _, offset_y = from_ratio(0, 0.05)
            self.elements.append(
                Button(
                    x=left+a, y=window.height - a - top - offset * i,
                    width=width, height=height,
                    color=(60, 60, 60),
                    text=world_data['name'], font_size=48,
                    on_hover=on_hover,
                    on_click=on_click,
                    data={"world_name": world_data['name']}
                )
            )

        def on_hover(button):
            button.color = (100, 100, 100)
        def on_click(button):
            self.ui_manager.game.change_scene("main_menu_scene")

        width, height = from_ratio(0.3, 0.05)
        x, _ = center(width, height)
        self.elements.append(
            Button(
                x=x, y=50,
                width=width, height=height,
                color=(60, 60, 60),
                text="назад", font_size=48,
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