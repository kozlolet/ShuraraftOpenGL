import math
import numpy as np


def view_matrix(camera_pos, yaw, pitch, player_height):
    translation = translate(camera_pos, player_height)                 # переносим мир в систему координат камеры
    yaw_rotation = rotate_y(-yaw)                       # Y rotation
    pitch_rotation = rotate_x(-pitch)                   # X rotation
    return pitch_rotation @ yaw_rotation @ translation


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


def translate(camera_pos, player_height):
    return np.array([
        [1, 0, 0, -camera_pos[0]],
        [0, 1, 0, -(camera_pos[1] + player_height)],
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


def perspective(fov, aspect, near, far):
    f = 1.0 / math.tan(fov / 2.0)
    return np.array([
        [f / aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far + near) / (near - far), (2 * far * near) / (near - far)],
        [0, 0, -1, 0],
    ], dtype='f4')


# def ortho(left, right, bottom, top, near=-1.0, far=1.0):
#     return np.array([
#         [2 / (right - left), 0, 0, -(right + left) / (right - left)],
#         [0, 2 / (top - bottom), 0, -(top + bottom) / (top - bottom)],
#         [0, 0, -2 / (far - near), -(far + near) / (far - near)],
#         [0, 0, 0, 1],
#     ], dtype='f4')

def ortho():
    return np.array([
        [2, 0, 0, -1],
        [0, 2, 0, -1],
        [0, 0, 2, -1],
        [0, 0, 0, 1],
    ], dtype='f4')