import numpy as np
from src.render.matrices import *


def calculate_mvp(window, player):
    aspect = window.width / window.height
    proj = perspective(math.radians(60), aspect, 0.1, 100.0)

    view = view_matrix(player.pos, player.yaw, player.pitch, player.height)
    model = matrix_polygon()

    return proj @ view @ model