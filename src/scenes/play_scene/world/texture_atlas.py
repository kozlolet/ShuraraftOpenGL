import numpy as np
import moderngl
from src.scenes.play_scene.world.blocks_config import BLOCKS
from PIL import Image


class TextureAtlas:
    def __init__(self, world):
        self.world = world
        self.atlas = None
        self.textures_count = None
        self.load_textures()

    def load_textures(self):
        textures_path = self.world.src_path / "textures" / "blocks"
        textures = []
        atlas_width = 64
        atlas_height = 0
        self.textures_count = 0
        for block_id in BLOCKS.keys():
            texture_name = BLOCKS[block_id]['texture']
            img = Image.open(textures_path / f'{texture_name}.png').convert("RGBA")
            arr = np.array(img, dtype=np.uint8)
            texture_height = len(arr)
            atlas_height += texture_height
            textures.append(arr.flatten())
            self.textures_count += 1

        atlas_data = np.array(textures, dtype=np.uint8).flatten()
        self.atlas = self.world.ctx.texture((atlas_width, atlas_height), 4, atlas_data.tobytes())
        self.atlas.filter = (moderngl.NEAREST, moderngl.NEAREST)

