def init_program(ctx):
    return ctx.program(
        vertex_shader='''
        #version 330

        uniform mat4 proj;
        in vec2 in_position;
        
        void main() {
            gl_Position = proj * vec4(in_position, 0.0, 1.0);
        }
    ''',
        fragment_shader='''
        #version 330

        uniform vec4 color;
        out vec4 fragColor;
        
        void main() {
            fragColor = color;
        }
    '''
    )