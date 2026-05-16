class Rect:
    def __init__(self, screen, x_ratio, y_ratio, width_ratio, height_ratio, color):
        self.x_ratio = x_ratio
        self.y_ratio = y_ratio
        self.width_ratio = width_ratio
        self.height_ratio = height_ratio
        self.color = color

        self.render = screen.render
        self.window = screen.ui_manager.window

    def mouse_in(self, mouse_x, mouse_y):
        x = self.x_ratio * self.window.width
        y = self.y_ratio * self.window.height
        width = self.width_ratio * self.window.width
        height = self.height_ratio * self.window.height
        if (x < mouse_x < x + width and
            y < mouse_y < y + height):
            return True
        else:
            return False

    def draw(self):
        self.render.draw_rect(x=self.x_ratio,
                              y=self.y_ratio,
                              w=self.width_ratio,
                              h=self.height_ratio,
                              color_255=self.color)
