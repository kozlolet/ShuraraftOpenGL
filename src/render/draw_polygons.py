from src.render.mvp import calculate_mvp
import pyglet
import moderngl


def draw_polygons(window, player, program, vao, texture_atlas):
    texture_atlas.use(0)
    program['tex'] = 0

    mvp = calculate_mvp(window=window,
                        player=player)

    program['mvp'].write(mvp.T.tobytes())

    vao.render(moderngl.TRIANGLES)