from pyglet.window import key
from pyglet.window import mouse
import math
import numpy as np
from src.physics.aabb import AABB
from src.physics.collision import move_entity
from src.scenes.play_scene.player.player_interaction import PlayerInteraction
from src.scenes.play_scene.player.sun import Sun


class Player:
    def __init__(self, play_scene):
        self.play_scene = play_scene
        self.ctx = play_scene.ctx
        self.keys = play_scene.game.keys
        self.interaction = PlayerInteraction(self)
        # self.sun = Sun(self)

        self.pos = np.array([10.0, 50.0, 20.0], dtype='f4')
        self.move_speed = 4.3
        self.run_speed = 5.6
        self.height = 1.62
        self.yaw = -math.radians(0)
        self.pitch = math.radians(0)
        self.turn_speed = math.radians(90)
        self.pitch_limit = math.radians(89)
        self.mouse_sensitivity = 0.001
        self.g = 10
        self.vertical_speed = 0
        self.jump_speed = 5
        self.onGround = False
        self.onShift = False
        self.movement_delta = np.array([0.0, 0.0, 0.0], dtype='f4')
        self.hitboxes = [
            AABB(-0.3, 0.0, -0.3, 0.3, 1.8, 0.3),
        ]
        self.arm_length = 5

    def mouse_motion(self, x, y, dx, dy):
        self.yaw -= dx * self.mouse_sensitivity
        self.pitch -= dy * self.mouse_sensitivity
        self.pitch = max(-self.pitch_limit, min(self.pitch_limit, self.pitch))

    def mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            self.interaction.mining()
        if button == mouse.RIGHT:
            self.interaction.putting()

    def update_keys_release(self, symbol, modifiers):
        pass

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

        forward = self.interaction.forward_vector()
        right = self.interaction.right_vector()

        if keys[key.W]:
            self.movement_delta += forward * self.move_speed * dt
        if keys[key.S]:
            self.movement_delta -= forward * self.move_speed * dt
        if keys[key.A]:
            self.movement_delta -= right * self.move_speed * dt
        if keys[key.D]:
            self.movement_delta += right * self.move_speed * dt
        if keys[key.SPACE]:
            if self.onGround:
                self.vertical_speed += self.jump_speed
                self.onGround = False
        if keys[key.LSHIFT]:
            self.onShift = True
            self.move_speed = 1.3
            self.height = 1.27
            self.hitboxes = [
                AABB(-0.3, 0.0, -0.3, 0.3, 1.5, 0.3),
            ]
        else:
            self.onShift = False
            self.move_speed = 4.3
            self.height = 1.62
            self.hitboxes = [
                AABB(-0.3, 0.0, -0.3, 0.3, 1.8, 0.3),
            ]

    def gravity(self, dt):
        self.vertical_speed -= self.g * dt
        self.movement_delta += self.interaction.up_vector() * self.vertical_speed * dt

    def update(self, dt):
        self.update_keys_press(dt)
        self.gravity(dt)
        move_entity(self, self.movement_delta)
        self.movement_delta *= 0

