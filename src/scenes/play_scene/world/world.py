from src.render.polygons import polygon_program
from pathlib import Path
from src.scenes.play_scene.world.block import Block
from src.scenes.play_scene.world.world_storage import WorldStorage
from src.scenes.play_scene.world.texture_atlas import TextureAtlas


class World:
    def __init__(self, play_scene):
        self.play_scene = play_scene
        self.ctx = play_scene.ctx

        self.world_name = self.play_scene.world_name
        self.src_path = Path(__file__).resolve().parent.parent.parent.parent
        self.program = polygon_program.init_program(self.ctx)

        self.texture_atlas = TextureAtlas(self)

        self.chunks = []
        self.storage = WorldStorage(self)
        self.storage.load_chunks()

    def get_block(self, x, y, z):
        if not 0 <= y <= 255: return

        chunk_x = x//16
        segment = y//16
        chunk_z = z//16

        in_chunk_x = x - 16*chunk_x
        in_segment_y = y - 16*segment
        in_chunk_z = z - 16*chunk_z

        chunk = next((chunk for chunk in self.chunks if chunk.x == chunk_x and chunk.z == chunk_z), None)
        if not chunk:
            return

        return chunk.blocks[segment][in_segment_y][in_chunk_x][in_chunk_z]

    def set_block(self, x, y, z, block_id):
        if not 0 <= y <= 255: return

        chunk_x = x//16
        segment = y//16
        chunk_z = z//16

        in_chunk_x = x - 16*chunk_x
        in_segment_y = y - 16*segment
        in_chunk_z = z - 16*chunk_z

        chunk = next((chunk for chunk in self.chunks if chunk.x == chunk_x and chunk.z == chunk_z), None)
        if not chunk:
            return

        block = Block(chunk, block_id, in_chunk_x, in_segment_y, in_chunk_z, segment)
        chunk.blocks[segment][in_segment_y][in_chunk_x][in_chunk_z] = block

        return block



    def update_block_chunks(self, block):
        block.chunk.make_polygons_vao()
        if block.z == 15:
            forward_chunk = next((chunk for chunk in self.chunks if chunk.x == block.chunk.x and chunk.z == block.chunk.z+1), None)
            if forward_chunk:
                forward_chunk.make_polygons_vao()
        if block.z == 0:
            back_chunk = next((chunk for chunk in self.chunks if chunk.x == block.chunk.x and chunk.z == block.chunk.z-1), None)
            if back_chunk:
                back_chunk.make_polygons_vao()
        if block.x == 15:
            right_chunk = next((chunk for chunk in self.chunks if chunk.x == block.chunk.x+1 and chunk.z == block.chunk.z), None)
            if right_chunk:
                right_chunk.make_polygons_vao()
        if block.x == 0:
            left_chunk = next((chunk for chunk in self.chunks if chunk.x == block.chunk.x-1 and chunk.z == block.chunk.z), None)
            if left_chunk:
                left_chunk.make_polygons_vao()

    # def mining_block(self, x, y, z):
    #     if not 0 <= y <= 63: return
    #
    #     chunk_x = x//16
    #     segment = y//16
    #     chunk_z = z//16
    #
    #     in_chunk_x = x - 16*chunk_x
    #     in_segment_y = y - 16*segment
    #     in_chunk_z = z - 16*chunk_z
    #
    #     chunk = next((chunk for chunk in self.chunks if chunk.x == chunk_x and chunk.z == chunk_z), None)
    #     if not chunk:
    #         return
    #
    #     chunk.blocks[segment][in_segment_y][in_chunk_x].pop(in_chunk_z)
    #     chunk.blocks[segment][in_segment_y][in_chunk_x].insert(in_chunk_z, 0)
    #
    #     # update chunks
    #     chunk.make_polygons_vao()
    #     if in_chunk_z == 15:
    #         forward_chunk = next((chunk for chunk in self.chunks if chunk.x == chunk_x and chunk.z == chunk_z+1), None)
    #         if forward_chunk:
    #             forward_chunk.make_polygons_vao()
    #     if in_chunk_z == 0:
    #         back_chunk = next((chunk for chunk in self.chunks if chunk.x == chunk_x and chunk.z == chunk_z-1), None)
    #         if back_chunk:
    #             back_chunk.make_polygons_vao()
    #     if in_chunk_x == 15:
    #         right_chunk = next((chunk for chunk in self.chunks if chunk.x == chunk_x+1 and chunk.z == chunk_z), None)
    #         if right_chunk:
    #             right_chunk.make_polygons_vao()
    #     if in_chunk_x == 0:
    #         left_chunk = next((chunk for chunk in self.chunks if chunk.x == chunk_x-1 and chunk.z == chunk_z), None)
    #         if left_chunk:
    #             left_chunk.make_polygons_vao()

    # def putting_block(self, x, y, z):
    #     if not 0 <= y <= 63: return
    #
    #     chunk_x = x//16
    #     segment = y//16
    #     chunk_z = z//16
    #
    #     in_chunk_x = x - 16*chunk_x
    #     in_segment_y = y - 16*segment
    #     in_chunk_z = z - 16*chunk_z
    #
    #     chunk = next((chunk for chunk in self.chunks if chunk.x == chunk_x and chunk.z == chunk_z), None)
    #     if not chunk:
    #         return
    #
    #     chunk.blocks[segment][in_segment_y][in_chunk_x].pop(in_chunk_z)
    #     chunk.blocks[segment][in_segment_y][in_chunk_x].insert(in_chunk_z, Block(chunk, 2, in_chunk_x, in_segment_y, in_chunk_z, segment))
    #
    #     chunk.make_polygons_vao()

    def update(self):
        pass

    def draw(self):
        for chunk in self.chunks:
            chunk.draw()