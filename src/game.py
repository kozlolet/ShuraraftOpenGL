import pyglet
import moderngl
from pyglet.window import key
from src.scenes.play_scene.play_scene import PlayScene
from src.render.matrices import perspective
import math
from src.render import mvp


class Game:
    def __init__(self):
        pyglet.options['shadow_window'] = False
        self.window = pyglet.window.Window(1200, 800, "3D MVP", resizable=True)

        self.keys = key.KeyStateHandler()
        # self.window.push_handlers(self.keys)
        self.window.set_exclusive_mouse(True)

        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.DEPTH_TEST)

        self.scene = PlayScene(self)

    def update(self, dt):
        self.scene.update(dt)

    def run(self):
        pyglet.clock.schedule_interval(self.update, 1 / 120)

        @self.window.event
        def on_draw():
            self.scene.draw()

        @self.window.event
        def on_resize(width, height):
            self.scene.ui.reload_uv()
            return pyglet.event.EVENT_HANDLED

        @self.window.event
        def on_mouse_motion(x, y, dx, dy):
            self.scene.mouse_motion(x, y, dx, dy)

        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            self.scene.mouse_press(x, y, button, modifiers)

        @self.window.event
        def on_key_press(symbol, modifiers):
            self.keys.on_key_press(symbol, modifiers)
            self.scene.key_press(symbol, modifiers)

        @self.window.event
        def on_key_release(symbol, modifiers):
            self.keys.on_key_release(symbol, modifiers)
            self.scene.key_release(symbol, modifiers)

        pyglet.app.run()

