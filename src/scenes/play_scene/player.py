from pyglet.window import key
from pyglet.window import mouse
import math
import numpy as np
from math import floor, degrees, sin, cos


class Player:
    def __init__(self, play_scene):
        self.play_scene = play_scene
        self.keys = play_scene.game.keys

        self.pos = np.array([10.0, 50.0, 20.0], dtype='f4')
        self.move_speed = 4.0
        self.height = 1.80
        self.yaw = -math.radians(90)
        self.pitch = math.radians(20)
        self.turn_speed = math.radians(90)
        self.pitch_limit = math.radians(89)
        self.mouse_sensitivity = 0.003
        self.gravity = 0.2
        self.vertical_speed = 0
        self.jump_speed = 8
        self.onGround = False

    def mouse_motion(self, x, y, dx, dy):
        self.yaw -= dx * self.mouse_sensitivity
        self.pitch -= dy * self.mouse_sensitivity
        self.pitch = max(-self.pitch_limit, min(self.pitch_limit, self.pitch))

    def mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            max_mining_distance = 8
            scale = 10

            for step in range(max_mining_distance * scale + 1):
                block_pos = self.pos + self.look_vector() * (step / scale)
                block_x = floor(block_pos[0])
                block_y = floor(block_pos[1] + self.height)
                block_z = floor(block_pos[2])

                if self.play_scene.world.get_block(block_x, block_y, block_z):
                    self.play_scene.world.mining_block(block_x, block_y, block_z)
                    break

        if button == mouse.RIGHT:
            max_putting_distance = 8
            scale = 10

            for step in range(max_putting_distance * scale + 1):
                block_pos = self.pos + self.look_vector() * (step / scale)
                block_x = floor(block_pos[0])
                block_y = floor(block_pos[1] + self.height)
                block_z = floor(block_pos[2])

                if self.play_scene.world.get_block(block_x, block_y, block_z):
                    next_block_pos = self.pos + (self.look_vector() * ((step-1) / scale))
                    next_block_x = floor(next_block_pos[0])
                    next_block_y = floor(next_block_pos[1] + self.height)
                    next_block_z = floor(next_block_pos[2])
                    print(f'{next_block_x} {next_block_y} {next_block_z}')
                    self.play_scene.world.putting_block(next_block_x, next_block_y, next_block_z)
                    break


    def look_vector(self):
        return np.array([
            -cos(self.pitch) * sin(self.yaw),
            -sin(self.pitch),
            -cos(self.pitch) * cos(self.yaw),
        ], dtype='f4')

    def forward_vector(self):
        return np.array([
            -sin(self.yaw),
            0.0,
            -cos(self.yaw),
        ], dtype='f4')

    def right_vector(self):
        return np.array([
            cos(self.yaw),
            0.0,
            -sin(self.yaw),
        ], dtype='f4')

    def update_keys_release(self, symbol, modifiers):
        pass
        # if symbol == key.SPACE:
        #     if not self.onGround:
        #         return
        #     self.vertical_speed += self.jump_speed
        #     self.onGround = False

    def update_keys_press(self, dt):
        keys = self.keys

        if keys[key.LEFT]:
            self.yaw += self.turn_speed * dt
        if keys[key.RIGHT]:
            self.yaw -= self.turn_speed * dt
        if keys[key.UP]:
            self.pitch -= self.turn_speed * dt
        if keys[key.DOWN]:
            self.pitch += self.turn_speed * dt

        self.pitch = max(-self.pitch_limit, min(self.pitch_limit, self.pitch))

        forward = self.forward_vector()
        right = self.right_vector()

        if keys[key.W]:
            self.pos += forward * self.move_speed * dt
        if keys[key.S]:
            self.pos -= forward * self.move_speed * dt
        if keys[key.A]:
            self.pos -= right * self.move_speed * dt
        if keys[key.D]:
            self.pos += right * self.move_speed * dt
        if keys[key.SPACE]:
            if self.onGround:
                self.vertical_speed += self.jump_speed
                self.onGround = False
        if keys[key.LSHIFT]:
            self.pos[1] -= self.move_speed * dt

    def update_physics(self, dt):
        get_block = self.play_scene.world.get_block
        x = floor(self.pos[0])
        y = floor(self.pos[1])
        z = floor(self.pos[2])

        player_on_block = get_block(x, y-1, z) and self.pos[1] == y and self.vertical_speed <= 0
        player_in_block = get_block(x, y, z)

        if player_in_block:
            if not self.onGround:
                self.pos[1] = y+1
                self.vertical_speed = 0
                self.onGround = True
        elif not player_on_block:
            self.vertical_speed -= self.gravity
            self.pos[1] += self.vertical_speed * dt
            self.onGround = False

    def update(self, dt):
        self.update_keys_press(dt)
        self.update_physics(dt)
