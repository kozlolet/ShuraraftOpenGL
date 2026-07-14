import numpy as np

from src.scenes.play_scene.world.block import Block
from src.render.polygons.split_block_on_polygons import split_block_on_polygons
from src.render.polygons.draw_polygons import draw_polygons


class Chunk:
    def __init__(self, world_storage, x, z):
        self.world_storage = world_storage
        self.world = world_storage.world

        self.ctx = self.world.ctx
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
        chunk_path = src_path / 'worlds' / self.world.world_name / f'chunk({self.x},{self.z})'
        with open(chunk_path / 'blocks.data', 'rb') as file:
            for s in range(16):
                self.blocks.append([])
                for y in range(16):
                    self.blocks[s].append([])
                    for x in range(16):
                        self.blocks[s][y].append([])
                        for z in range(16):
                            block_id = file.read(1)
                            int_block_id = int.from_bytes(block_id)
                            if int_block_id:
                                self.blocks[s][y][x].append(Block(self, int_block_id, x, y, z, s))
                            else:
                                self.blocks[s][y][x].append(0)

    def make_polygons_vao(self):
        polygons_mesh = []
        for s in range(16):
            for y in range(16):
                for x in range(16):
                    for z in range(16):
                        block = self.blocks[s][y][x][z]
                        if not block:
                            continue

                        polygons = split_block_on_polygons(block=block,
                                                           textures_count=self.world.texture_atlas.textures_count)

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
                      texture_atlas=self.world.texture_atlas.atlas)
