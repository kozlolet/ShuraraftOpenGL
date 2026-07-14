import numpy as np
from src.render.sky import sky_program
import moderngl

class SkyRender:
    def __init__(self, ctx, bottom_color=(0.7, 0.9, 1.0), top_color=(0.2, 0.5, 1.0)):
        self.ctx = ctx
        self.bottom_color = bottom_color
        self.top_color = top_color

        vertices = np.array([
            -1.0, -1.0,
            1.0, -1.0,
            1.0,  1.0,

            -1.0, -1.0,
            1.0,  1.0,
            -1.0,  1.0,
        ], dtype='f4')
        self.vbo = self.ctx.buffer(vertices.tobytes())
        self.program = sky_program.init_program(ctx)
        self.vao = self.ctx.vertex_array(
            self.program,
            [(self.vbo, '2f', 'in_position')]
        )
        self.program['bottom_color'].value = bottom_color
        self.program['top_color'].value = top_color

    def draw(self):
        self.ctx.disable(moderngl.DEPTH_TEST)
        self.vao.render(moderngl.TRIANGLES)
        self.ctx.enable(moderngl.DEPTH_TEST)

