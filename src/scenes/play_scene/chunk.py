import os
from pprint import pprint
from pathlib import Path

import numpy as np

from src.scenes.play_scene.block import Block
from src.render.split_block_on_polygons import split_block_on_polygons
from src.render.draw_polygons import draw_polygons



class Chunk:
    def __init__(self, world, x, z):
        self.ctx = world.ctx
        self.world = world
        self.x = x
        self.z = z
        self.blocks = []
        self.load_blocks()
        self.polygons_vbo = None
        self.polygons_vao = None

    def load_blocks(self):
        self.blocks = []
        src_path = self.world.src_path
        # src_path = Path(__file__).resolve().parent.parent.parent
        chunk_path = src_path / 'worlds' / 'ivan' / f'chunk({self.x},{self.z})'
        with open(chunk_path / 'blocks.data', 'rb') as file:
            for y in range(64):
                self.blocks.append([])
                for x in range(16):
                    self.blocks[y].append([])
                    for z in range(16):
                        block_id = file.read(1)
                        int_block_id = int.from_bytes(block_id)
                        if int_block_id:
                            self.blocks[y][x].append(Block(self, int_block_id, x, y, z))
                        else:
                            self.blocks[y][x].append(0)

    def make_polygons_vao(self):
        polygons_mesh = []
        for y in range(64):
            for x in range(16):
                for z in range(16):
                    block = self.blocks[y][x][z]
                    if not block:
                        continue

                    polygons = split_block_on_polygons(block=block,
                                                       textures_count=self.world.textures_count)

                    polygons_mesh.extend(polygons)

        polygons_arr = np.array(polygons_mesh, dtype='f4').flatten()
        self.polygons_vbo = self.ctx.buffer(polygons_arr.tobytes())

        self.polygons_vao = self.ctx.vertex_array(
            self.world.program,
            [(self.polygons_vbo, '3f 2f', 'in_position', 'in_uv')]
        )

    def draw(self):
        draw_polygons(window=self.world.play_scene.game.window,
                      player=self.world.play_scene.player,
                      program=self.world.program,
                      vao=self.polygons_vao,
                      texture_atlas=self.world.texture_atlas)





# for mesh in self.meshes:
#     draw_polygon(ctx=self.ctx,
#                  window=self.play_scene.game.window,
#                  player=self.play_scene.player,
#                  program=self.program,
#                  vao=mesh['vao'],
#                  texture=texture)



# for chunk_x in range(4):
#     for chunk_z in range(4):
#         # chunk = Chunk(1, chunk_x, chunk_z)
#         src_path = Path(__file__).resolve().parent.parent.parent
#         chunk_path = src_path / 'worlds' / 'ivan' / f'chunk({chunk_x},{chunk_z})'
#         os.makedirs(chunk_path)
#         with open(chunk_path / 'blocks.data', 'wb') as file:
#             for y in range(16):
#                 for x in range(16):
#                     for z in range(16):
#                         block = 1
#                         file.write(block.to_bytes())


# src_path = Path(__file__).resolve().parent.parent.parent
# world_path = src_path / 'worlds' / 'ivan' / 'chunk(0,0)'
# with open(world_path / 'blocks.data', 'wb') as file:
#     block = 1
#     file.write(block.to_bytes())

