from src.game import Game
import pyglet


if __name__ == '__main__':
    game = Game()
    game.run()
    # pyglet.clock.schedule_interval(game.update, 1 / 120)
    # pyglet.app.run()

