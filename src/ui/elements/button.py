import pyglet


class Button:
    def __init__(self, x, y, width, height, color, text, font_size=48, on_hover=None, on_click=None, data=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.data = data

        self.text = text
        self.font_size = font_size

        self.rect = pyglet.shapes.Rectangle(x, y, width, height, color)
        self.label = pyglet.text.Label(
            text,
            x=x + width // 2,
            y=y + height // 2,
            z=1,
            anchor_x='center',
            anchor_y='center',
            font_size=font_size
        )

        self.is_hovered = False
        self.on_hover = on_hover
        self.on_click = on_click

        self.start_rect = self.rect
        self.start_label = self.label

    def contains_point(self, mouse_x, mouse_y):
        return (
            self.x <= mouse_x <= self.x + self.width and
            self.y <= mouse_y <= self.y + self.height
        )

    def mouse_motion(self, x, y):
        hovered_now = self.contains_point(x, y)

        if hovered_now and not self.is_hovered:
            self.is_hovered = True
            if self.on_hover is not None:
                self.on_hover(self)
                self.update_button()

        elif not hovered_now:
            self.is_hovered = False
            self.rect = self.start_rect
            self.label = self.start_label

    def mouse_release(self, x, y, button, modifiers):
        click = self.contains_point(x, y)

        if click:
            self.on_click(self)
            self.update_button()
        else:
            self.rect = self.start_rect
            self.label = self.start_label

    def update_button(self):
        self.rect = pyglet.shapes.Rectangle(self.x, self.y, self.width, self.height, self.color)
        self.label = pyglet.text.Label(
            self.text,
            x=self.x + self.width // 2, y=self.y + self.height // 2, z=1,
            anchor_x='center', anchor_y='center',
            font_size=self.font_size
        )

    def draw(self):
        self.rect.draw()
        self.label.draw()

