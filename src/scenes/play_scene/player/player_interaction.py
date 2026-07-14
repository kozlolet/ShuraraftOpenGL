from math import floor, cos, sin
import numpy as np
from src.scenes.play_scene.world.block import Block

class PlayerInteraction:
    def __init__(self, player):
        self.player = player
        self.world = player.play_scene.world

    def look_vector(self):
        return np.array([
            -cos(self.player.pitch) * sin(self.player.yaw),
            -sin(self.player.pitch),
            -cos(self.player.pitch) * cos(self.player.yaw),
            ], dtype='f4')

    def forward_vector(self):
        return np.array([
            -sin(self.player.yaw),
            0.0,
            -cos(self.player.yaw),
        ], dtype='f4')

    def right_vector(self):
        return np.array([
            cos(self.player.yaw),
            0.0,
            -sin(self.player.yaw),
        ], dtype='f4')

    def up_vector(self):
        return np.array([
            0,
            1,
            0
        ], dtype='f4')

    def mining(self):
        scale = 10
        for step in range(self.player.arm_length * scale + 1):

            ray_pos = self.player.pos + self.look_vector() * (step / scale)

            ray_x = floor(ray_pos[0])
            ray_y = floor(ray_pos[1] + self.player.height)
            ray_z = floor(ray_pos[2])

            block = self.world.get_block(ray_x, ray_y, ray_z)
            if block:
                block.chunk.blocks[block.s][block.y][block.x][block.z] = 0
                self.world.update_block_chunks(block)
                break

    def putting(self):
        scale = 10

        for step in range(self.player.arm_length * scale + 1):

            ray_pos = self.player.pos + self.look_vector() * (step / scale)

            ray_x = floor(ray_pos[0])
            ray_y = floor(ray_pos[1] + self.player.height)
            ray_z = floor(ray_pos[2])

            if self.player.play_scene.world.get_block(ray_x, ray_y, ray_z):

                block_pos = self.player.pos + (self.look_vector() * ((step-1) / scale))

                block_x = floor(block_pos[0])
                block_y = floor(block_pos[1] + self.player.height)
                block_z = floor(block_pos[2])

                block = self.world.set_block(block_x, block_y, block_z, 2)
                if block:
                    self.world.update_block_chunks(block)
                    break


