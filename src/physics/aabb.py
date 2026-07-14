from math import floor, ceil


class AABB:
    def __init__(self, min_x, min_y, min_z, max_x, max_y, max_z):
        self.min_x = min_x
        self.min_y = min_y
        self.min_z = min_z
        self.max_x = max_x
        self.max_y = max_y
        self.max_z = max_z

def global_aabb(aabb, pos):  # дает глобальные координаты хитбокса
    return AABB(
        aabb.min_x + pos[0],
        aabb.min_y + pos[1],
        aabb.min_z + pos[2],
        aabb.max_x + pos[0],
        aabb.max_y + pos[1],
        aabb.max_z + pos[2],
    )

def intersects(a, b):  # проверяет на пересечение хитбоксов
    return (
        a.min_x < b.max_x and a.max_x > b.min_x and
        a.min_y < b.max_y and a.max_y > b.min_y and
        a.min_z < b.max_z and a.max_z > b.min_z
    )

def block_aabb(x, y, z):  # задает хитбокс стандартному блоку
    return AABB(x, y, z, x + 1, y + 1, z + 1)

def get_blocks_overlapping_aabb(world, box):  # выделяет те блоки которые окружают чей-то хитбокс
    min_x = floor(box.min_x)
    max_x = ceil(box.max_x)
    min_y = floor(box.min_y)
    max_y = ceil(box.max_y)
    min_z = floor(box.min_z)
    max_z = ceil(box.max_z)

    blocks = []

    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            for z in range(min_z, max_z):
                if world.get_block(x, y, z):
                    blocks.append(block_aabb(x, y, z))

    return blocks