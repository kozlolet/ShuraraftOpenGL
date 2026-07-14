def init_program(ctx):
    return ctx.program(
        vertex_shader='''
        #version 330

        in vec2 in_position;
        out vec2 v_position;
        
        void main() {
            v_position = in_position;
            gl_Position = vec4(in_position, 0.0, 1.0);
        }
    ''',
        fragment_shader='''
        #version 330
        
        in vec2 v_position;
        
        uniform vec3 bottom_color;
        uniform vec3 top_color;
        
        out vec4 fragColor;
        
        void main() {
            float t = (v_position.y + 1.0) * 0.5;
            vec3 color = mix(bottom_color, top_color, t);
            fragColor = vec4(color, 1.0);
        }
    '''
    )