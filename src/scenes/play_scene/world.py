import numpy as np
from PIL import Image
import moderngl
from src.render import polygon_program
import os
from pathlib import Path
from src.scenes.play_scene.chunk import Chunk
from src.scenes.play_scene.textures_order import textures_order
from math import floor
from  src.scenes.play_scene.block import Block


class World:
    def __init__(self, play_scene):
        self.play_scene = play_scene
        self.ctx = play_scene.ctx

        self.src_path = Path(__file__).resolve().parent.parent.parent
        self.program = polygon_program.init_program(self.ctx)

        self.texture_atlas = None
        self.textures_count = None
        self.load_textures()

        self.chunks = []
        self.already_loaded_chunks_pos = []
        self.load_chunks()

    def load_chunks(self):
        world_path = self.src_path / 'worlds' / 'ivan'
        for name in os.listdir(world_path):
            full_path = os.path.join(world_path / name)
            if os.path.isdir(full_path):
                print(f'load {name}')
                x, z = map(int, name.replace('chunk(', '').replace(')', '').split(','))
                if [x, z] in self.already_loaded_chunks_pos:
                    continue

                chunk = Chunk(self, x, z)
                self.chunks.append(chunk)
                chunk.make_polygons_vao()

                self.already_loaded_chunks_pos.append([x, z])

    def load_textures(self):
        textures_path = self.src_path / "textures" / "blocks"
        textures = []
        atlas_width = 64
        atlas_height = 0
        self.textures_count = 0
        for texture_name in textures_order:
            img = Image.open(textures_path / f'{texture_name}.png').convert("RGBA")
            arr = np.array(img, dtype=np.uint8)
            texture_height = len(arr)
            atlas_height += texture_height
            textures.append(arr.flatten())
            self.textures_count += 1

        atlas_data = np.array(textures, dtype=np.uint8).flatten()
        self.texture_atlas = self.ctx.texture((atlas_width, atlas_height), 4, atlas_data.tobytes())
        self.texture_atlas.filter = (moderngl.NEAREST, moderngl.NEAREST)

    def get_block(self, x, y, z):
        if not 0 <= y <= 63: return

        chunk_x = x//16
        chunk_z = z//16
        in_chunk_x = x - 16*chunk_x
        in_chunk_y = y
        in_chunk_z = z - 16*chunk_z

        chunk = next((chunk for chunk in self.chunks if chunk.x == chunk_x and chunk.z == chunk_z), None)
        if not chunk:
            return

        return chunk.blocks[in_chunk_y][in_chunk_x][in_chunk_z]

    def mining_block(self, x, y, z):
        if not 0 <= y <= 63: return

        chunk_x = x//16
        chunk_z = z//16
        in_chunk_x = x - 16*chunk_x
        in_chunk_y = y
        in_chunk_z = z - 16*chunk_z

        chunk = next((chunk for chunk in self.chunks if chunk.x == chunk_x and chunk.z == chunk_z), None)
        if not chunk:
            return

        chunk.blocks[in_chunk_y][in_chunk_x].pop(in_chunk_z)
        chunk.blocks[in_chunk_y][in_chunk_x].insert(in_chunk_z, 0)

        # update chunks
        chunk.make_polygons_vao()
        if in_chunk_z == 15:
            forward_chunk = next((chunk for chunk in self.chunks if chunk.x == chunk_x and chunk.z == chunk_z+1), None)
            if forward_chunk:
                forward_chunk.make_polygons_vao()
        elif in_chunk_z == 0:
            back_chunk = next((chunk for chunk in self.chunks if chunk.x == chunk_x and chunk.z == chunk_z-1), None)
            if back_chunk:
                back_chunk.make_polygons_vao()
        elif in_chunk_x == 15:
            right_chunk = next((chunk for chunk in self.chunks if chunk.x == chunk_x+1 and chunk.z == chunk_z), None)
            if right_chunk:
                right_chunk.make_polygons_vao()
        elif in_chunk_z == 0:
            left_chunk = next((chunk for chunk in self.chunks if chunk.x == chunk_x-1 and chunk.z == chunk_z-1), None)
            if left_chunk:
                left_chunk.make_polygons_vao()

    def putting_block(self, x, y, z):
        if not 0 <= y <= 63: return

        chunk_x = x//16
        chunk_z = z//16
        in_chunk_x = x - 16*chunk_x
        in_chunk_y = y
        in_chunk_z = z - 16*chunk_z

        chunk = next((chunk for chunk in self.chunks if chunk.x == chunk_x and chunk.z == chunk_z), None)
        if not chunk:
            return

        chunk.blocks[in_chunk_y][in_chunk_x].pop(in_chunk_z)
        chunk.blocks[in_chunk_y][in_chunk_x].insert(in_chunk_z, Block(chunk, 2, in_chunk_x, in_chunk_y, in_chunk_z))

        chunk.make_polygons_vao()

    def update(self):
        pass

    def draw(self):
        for chunk in self.chunks:
            chunk.draw()