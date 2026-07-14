import os
from src.scenes.play_scene.world.chunk import Chunk

class WorldStorage:
    def __init__(self, world):
        self.world = world

        self.src_path = world.src_path
        self.already_loaded_chunks_pos = []

    def load_chunks(self):
        print('\033[34m')
        world_path = self.src_path / 'worlds' / self.world.world_name
        for name in os.listdir(world_path):
            full_path = os.path.join(world_path / name)
            if os.path.isdir(full_path):
                print(f'load {name}')
                x, z = map(int, name.replace('chunk(', '').replace(')', '').split(','))
                if [x, z] in self.already_loaded_chunks_pos:
                    continue

                chunk = Chunk(self, x, z)
                self.world.chunks.append(chunk)
                chunk.make_polygons_vao()

                self.already_loaded_chunks_pos.append([x, z])
        print('\033[0m')

    def save_world(self):
        print('\033[32m')
        def is_all_zeros(chunk, segment_num):
            for segment in chunk.blocks[segment_num:]:
                for y in range(16):
                    for x in range(16):
                        for z in range(16):
                            if segment[y][x][z] != 0:
                                return False
            return True

        world_path = self.src_path / 'worlds' / self.world.world_name
        for chunk in self.world.chunks:
            folder_name = f'chunk({chunk.x},{chunk.z})'
            print(f'save {folder_name}')
            with open(world_path / folder_name / 'blocks.data', 'wb') as file:
                for s in range(16):
                    if is_all_zeros(chunk, s):
                        break
                    for y in range(16):
                        for x in range(16):
                            for z in range(16):
                                block = chunk.blocks[s][y][x][z]
                                zero_bytes = int.to_bytes(0)
                                if block:
                                    file.write(block.id.to_bytes())
                                else:
                                    file.write(zero_bytes)
        print('\033[0m')