from pyglet.window import key
import math
import numpy as np


class Player:
    def __init__(self, play_scene):
        self.play_scene = play_scene
        self.keys = play_scene.game.keys

        self.pos = np.array([0.0, 5.0, 20.0], dtype='f4')
        self.move_speed = 4.0

        self.yaw = -math.radians(35)
        self.pitch = math.radians(20)
        self.turn_speed = math.radians(90)
        self.pitch_limit = math.radians(89)
        self.mouse_sensitivity = 0.003

    def mouse_handle(self, x, y, dx, dy):
        self.yaw -= dx * self.mouse_sensitivity
        self.pitch -= dy * self.mouse_sensitivity
        self.pitch = max(-self.pitch_limit, min(self.pitch_limit, self.pitch))

    def forward_vector(self):
        return np.array([
            -math.sin(self.yaw),
            0.0,
            -math.cos(self.yaw),
        ], dtype='f4')

    def right_vector(self):
        return np.array([
            math.cos(self.yaw),
            0.0,
            -math.sin(self.yaw),
        ], dtype='f4')

    def update(self, dt):
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
            self.pos[1] += self.move_speed * dt
        if keys[key.LSHIFT]:
            self.pos[1] -= self.move_speed * dt