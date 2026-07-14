import numpy as np
from src.render.polygons.draw_polygons import draw_polygons


class Sun:
    def __init__(self, player):
        self.player = player
        self.ctx = player.ctx
        self.program = player.play_scene.world.program
        self.window = player.play_scene.window
        self.pos = self.player.pos + np.array([0, 0, 10], dtype='f4')

    def make_vao(self):
        x, y, z = self.pos[0], self.pos[1], self.pos[2]
        vertices = np.array([
            x,   y,   z,   0, 0,
            x,   y+1, z,   0, 1,
            x+1, y+1, z,   1, 1,

            x,   y,   z,   0, 0,
            x+1, y,   z,   1, 0,
            x+1, y+1, z,   1, 1,
        ], dtype='f4')
        self.vbo = self.ctx.buffer(vertices.tobytes())

        self.vao = self.ctx.vertex_array(
            self.program,
            [(self.vbo, '3f 2f', 'in_position', 'in_uv')]
        )

    def draw(self):
        self.vao
