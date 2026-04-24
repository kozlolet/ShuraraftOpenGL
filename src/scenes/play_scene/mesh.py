class Mesh:
    def __init__(self, ctx, program, vertices):
        self.vbo = ctx.buffer(vertices.tobytes())
        self.vao = ctx.vertex_array(
            program,
            [(self.vbo, '3f 2f', 'in_position', 'in_uv')]
        )

    def render(self):
        self.vao.render()