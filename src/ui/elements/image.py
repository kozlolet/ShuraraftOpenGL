import pyglet


class Image:
    def __init__(self, image, x, y, width=None, height=None, scale=1, on_hover=None, on_click=None):
        self.x = x
        self.y = y
        self.image = image

        self.sprite = pyglet.sprite.Sprite(image, x, y)
        self.sprite.scale = scale

        self.sprite.width = width if width else self.sprite.width
        self.sprite.height = height if height else self.sprite.height

        self.on_hover = on_hover
        self.on_click = on_click

        self.start_sprite = self.sprite

    def contains_point(self, mouse_x, mouse_y):
        return (
            self.x <= mouse_x <= self.x + self.sprite.width and
            self.y <= mouse_y <= self.y + self.sprite.height
        )

    def mouse_motion(self, x, y):
        hovered_now = self.contains_point(x, y)

        if hovered_now and not self.is_hovered:
            self.is_hovered = True
            if self.on_hover is not None:
                self.on_hover(self)

        elif not hovered_now:
            self.is_hovered = False
            self.sprite = self.start_sprite

    def mouse_release(self, x, y, button, modifiers):
        click = self.contains_point(x, y)

        if click:
            self.on_click(self)
        else:
            self.sprite = self.start_sprite

    def draw(self):
        self.sprite.draw()

