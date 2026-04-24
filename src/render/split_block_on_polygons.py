import numpy as np


def split_block_on_polygons(block, textures_count):
    world = block.chunk.world

    x = block.x + 16*block.chunk.x  # absolute
    y = block.y                     # absolute
    z = block.z + 16*block.chunk.z  # absolute

    texture_num = block.id
    v_atlas = lambda v_local: (texture_num-1) * (1.0 / textures_count) + v_local * (1.0 / textures_count)

    v0 = v_atlas(0)
    v1 = v_atlas(1)
    polygons = []

    def append_triangle(p1, uv1, p2, uv2, p3, uv3):
        nonlocal polygons
        polygons.extend([
            p1[0], p1[1], p1[2], uv1[0], uv1[1],
            p2[0], p2[1], p2[2], uv2[0], uv2[1],
            p3[0], p3[1], p3[2], uv3[0], uv3[1],
        ])

    # -Z face
    if not world.get_block(x, y, z-1):
        append_triangle(
            [x+1, y, z], [1, v1],
            [x, y+1, z], [0, v0],
            [x, y, z],   [0, v1],
        )
        append_triangle(
            [x+1, y, z],   [1, v1],
            [x, y+1, z],   [0, v0],
            [x+1, y+1, z], [1, v0],
        )

    # -X face
    if not world.get_block(x-1, y, z):
        append_triangle(
            [x, y, z],     [1, v1],
            [x, y+1, z+1], [0, v0],
            [x, y, z+1],   [0, v1],
        )
        append_triangle(
            [x, y, z],     [1, v1],
            [x, y+1, z+1], [0, v0],
            [x, y+1, z],   [1, v0],
        )

    # +X face
    if not world.get_block(x+1, y, z):
        append_triangle(
            [x+1, y+1, z], [0, v0],
            [x+1, y, z+1], [1, v1],
            [x+1, y, z],   [0, v1],
        )
        append_triangle(
            [x+1, y+1, z],   [0, v0],
            [x+1, y, z+1],   [1, v1],
            [x+1, y+1, z+1], [1, v0],
        )

    # +Z face
    if not world.get_block(x, y, z+1):
        append_triangle(
            [x, y+1, z+1], [1, v0],
            [x+1, y, z+1], [0, v1],
            [x, y, z+1],   [1, v1],
        )
        append_triangle(
            [x, y+1, z+1],   [1, v0],
            [x+1, y, z+1],   [0, v1],
            [x+1, y+1, z+1], [0, v0],
        )

    # -Y face (низ)
    if not world.get_block(x, y-1, z):
        append_triangle(
            [x, y, z+1], [0, v1],
            [x+1, y, z], [1, v0],
            [x, y, z],   [0, v0],
        )
        append_triangle(
            [x, y, z+1],   [0, v1],
            [x+1, y, z],   [1, v0],
            [x+1, y, z+1], [1, v1],
        )

    # +Y face (верх)
    if not world.get_block(x, y+1, z):
        append_triangle(
            [x, y+1, z+1], [0, v0],
            [x+1, y+1, z], [1, v1],
            [x, y+1, z],   [0, v1],
        )
        append_triangle(
            [x, y+1, z+1],   [0, v0],
            [x+1, y+1, z],   [1, v1],
            [x+1, y+1, z+1], [1, v0],
        )
    return polygons
