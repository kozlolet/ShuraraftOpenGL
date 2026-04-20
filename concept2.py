import pyglet
import moderngl
import numpy as np
import math
from pyglet.window import key
from PIL import Image


pyglet.options['shadow_window'] = False

window = pyglet.window.Window(1200, 800, "3D MVP", resizable=True)

keys = key.KeyStateHandler()
window.push_handlers(keys)

ctx = moderngl.create_context()
ctx.enable(moderngl.DEPTH_TEST)

vertices = np.array([
    -0.5, -0.5, 0.0,   0.0, 1.0,
    0.5, -0.5, 0.0,   1.0, 1.0,
    0.0,  0.5, 0.0,   0.5, 0.0,
], dtype='f4')

vbo = ctx.buffer(vertices.tobytes())

program = ctx.program(
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

vao = ctx.vertex_array(
    program,
    [(vbo, '3f 2f', 'in_position', 'in_uv')]
)

img = Image.open("ivan.png").convert("RGBA")
arr = np.array(img, dtype=np.uint8)          # shape: (height, width, 4)

texture_height = len(arr)
texture_width = len(arr[0])
tex_data = arr.flatten()

texture = ctx.texture((texture_width, texture_height), 4, tex_data.tobytes())
texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
texture.use(0)
program['tex'] = 0


def perspective(fov, aspect, near, far):
    f = 1.0 / math.tan(fov / 2.0)
    return np.array([
        [f / aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far + near) / (near - far), (2 * far * near) / (near - far)],
        [0, 0, -1, 0],
    ], dtype='f4')


def rotate_y(angle):
    c = math.cos(angle)
    s = math.sin(angle)
    return np.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1],
    ], dtype='f4')


def rotate_x(angle):
    c = math.cos(angle)
    s = math.sin(angle)
    return np.array([
        [1, 0, 0, 0],
        [0, c, s, 0],
        [0, -s, c, 0],
        [0, 0, 0, 1],
    ], dtype='f4')


def translate(camera_pos):
    return np.array([
        [1, 0, 0, -camera_pos[0]],
        [0, 1, 0, -camera_pos[1]],
        [0, 0, 1, -camera_pos[2]],
        [0, 0, 0, 1],
    ], dtype='f4')


def matrix_polygon():
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ], dtype='f4')


def view_matrix(camera_pos, yaw, pitch):
    translation = translate(camera_pos)  # переносим мир в систему координат камеры
    yaw_rotation = rotate_y(-yaw)             # Y rotation
    pitch_rotation = rotate_x(-pitch)         # X rotation
    return pitch_rotation @ yaw_rotation @ translation


aspect = window.width / window.height
proj = perspective(math.radians(60), aspect, 0.1, 100.0)

camera_pos = np.array([0.0, 0.0, 8.0], dtype='f4')
yaw = 0.0
pitch = 0.0

move_speed = 4.0
turn_speed = math.radians(90)
mouse_sensitivity = 0.003
pitch_limit = math.radians(89)

window.set_exclusive_mouse(True)


def forward_vector(yaw_angle):
    return np.array([
        -math.sin(yaw_angle),
        0.0,
        -math.cos(yaw_angle),
    ], dtype='f4')


def right_vector(yaw_angle):
    return np.array([
        math.cos(yaw_angle),
        0.0,
        -math.sin(yaw_angle),
    ], dtype='f4')


def update(dt):
    global camera_pos, yaw, pitch

    if keys[key.LEFT]:
        yaw += turn_speed * dt
    if keys[key.RIGHT]:
        yaw -= turn_speed * dt
    if keys[key.UP]:
        pitch -= turn_speed * dt
    if keys[key.DOWN]:
        pitch += turn_speed * dt

    pitch = max(-pitch_limit, min(pitch_limit, pitch))

    forward = forward_vector(yaw)
    right = right_vector(yaw)

    if keys[key.W]:
        camera_pos += forward * move_speed * dt
    if keys[key.S]:
        camera_pos -= forward * move_speed * dt
    if keys[key.A]:
        camera_pos -= right * move_speed * dt
    if keys[key.D]:
        camera_pos += right * move_speed * dt
    if keys[key.SPACE]:
        camera_pos[1] += move_speed * dt
    if keys[key.LSHIFT]:
        camera_pos[1] -= move_speed * dt


pyglet.clock.schedule_interval(update, 1 / 120)


@window.event
def on_mouse_motion(x, y, dx, dy):
    global yaw, pitch

    yaw -= dx * mouse_sensitivity
    pitch -= dy * mouse_sensitivity
    pitch = max(-pitch_limit, min(pitch_limit, pitch))


# @window.event
# def on_key_press(symbol, modifiers):
#     if symbol == key.ESCAPE:
#         window.set_exclusive_mouse(not window.exclusive)


@window.event
def on_resize(width, height):
    global proj
    ctx.viewport = (0, 0, width, height)
    aspect = width / max(height, 1)
    proj = perspective(math.radians(60), aspect, 0.1, 100.0)
    return pyglet.event.EVENT_HANDLED

@window.event
def on_draw():
    ctx.clear(0.1, 0.2, 0.3)

    view = view_matrix(camera_pos, yaw, pitch)
    model = matrix_polygon()

    mvp = proj @ view @ model
    program['mvp'].write(mvp.T.tobytes())

    vao.render(moderngl.TRIANGLES)


pyglet.app.run()
