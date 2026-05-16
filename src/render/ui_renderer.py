from src.render.matrices import ortho
from src.render.ui_program import init_program
import numpy as np
import moderngl


class UIRenderer:
    def __init__(self, ctx, window):
        self.ctx = ctx
        self.window = window
        self.program = init_program(ctx)
        self.proj = ortho()

    def draw_rect(self, x, y, w, h, color_255):
        vertices = np.array([
            x,      y,
            x+w,    y,
            x+w,    y+h,
            x,      y,
            x+w,    y+h,
            x,      y+h,
            ], dtype='f4')

        vbo = self.ctx.buffer(vertices.tobytes())
        vao = self.ctx.vertex_array(self.program, [(vbo, '2f', 'in_position')])

        self.program['proj'].write(self.proj.T.tobytes())
        color = [pigment/255 for pigment in color_255]
        self.program['color'].value = color

        vao.render()
