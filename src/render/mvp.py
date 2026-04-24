import numpy as np

from src.render.matrices import *

proj = np.array([])

def calculate_mvp(window, player):
    global proj

    if not proj.any():
        aspect = window.width / window.height
        proj = perspective(math.radians(60), aspect, 0.1, 100.0)

    view = view_matrix(player.pos, player.yaw, player.pitch)
    model = matrix_polygon()

    return proj @ view @ model