def init_program(ctx):
    return ctx.program(
        vertex_shader='''
        #version 330

        uniform mat4 mvp;

        in vec3 in_position;
        in vec2 in_uv;

        out vec2 v_uv;

        void main() {
            gl_Position = mvp * vec4(in_position, 1.0);
            v_uv = in_uv;
        }
    ''',
        fragment_shader='''
        #version 330

        uniform sampler2D tex;

        in vec2 v_uv;
        out vec4 fragColor;

        void main() {
            fragColor = texture(tex, v_uv);
        }
    '''
    )