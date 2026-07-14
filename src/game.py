import pyglet
import moderngl
from pyglet.window import key
from src.scenes.play_scene.play_scene import PlayScene
from src.scenes.main_menu_scene.main_menu_scene import MainMenuScene
from src.scenes.world_selection_scene.world_selection_scene import WorldSelectionScene


class Game:
    def __init__(self):
        pyglet.options['shadow_window'] = False
        self.window = pyglet.window.Window(1200, 800, "shuraraft", resizable=True)

        self.keys = key.KeyStateHandler()
        # self.window.push_handlers(self.keys)
        self.window.set_exclusive_mouse(True)

        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.DEPTH_TEST)

        self.scene_factories = {
            "main_menu_scene": lambda: MainMenuScene(self),
            "world_selection_scene": lambda: WorldSelectionScene(self),
            "play_scene": lambda world_name: PlayScene(self, world_name),
        }
        self.current_scene = self.scene_factories["main_menu_scene"]()

    def change_scene(self, name, agrs=()):
        self.current_scene = self.scene_factories[name](*agrs)

    def update(self, dt):
        self.current_scene.update(dt)

    def run(self):
        pyglet.clock.schedule_interval(self.update, 1 / 120)

        @self.window.event
        def on_draw():
            self.current_scene.draw()

        @self.window.event
        def on_resize(width, height):
            self.current_scene.ui.reload_uv()
            return pyglet.event.EVENT_HANDLED

        @self.window.event
        def on_mouse_motion(x, y, dx, dy):
            self.current_scene.mouse_motion(x, y, dx, dy)

        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            self.current_scene.mouse_press(x, y, button, modifiers)

        @self.window.event
        def on_mouse_release(x, y, button, modifiers):
            self.current_scene.mouse_release(x, y, button, modifiers)

        @self.window.event
        def on_key_press(symbol, modifiers):
            self.keys.on_key_press(symbol, modifiers)
            self.current_scene.key_press(symbol, modifiers)

        @self.window.event
        def on_key_release(symbol, modifiers):
            self.keys.on_key_release(symbol, modifiers)
            self.current_scene.key_release(symbol, modifiers)

        pyglet.app.run()

