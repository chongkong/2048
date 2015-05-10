import pyglet
from board import Board
from pyglet.window import key
from pyglet import clock


class Player:

    def __init__(self, size=4):
        self._size = size
        self._board = Board(size)

    def reset(self):
        self._board.reset()

    def on_key_press(self, symbol, modifiers):
        mapper = {
            key.LEFT: (-1, 0),
            key.RIGHT: (1, 0),
            key.UP: (0, 1),
            key.DOWN: (0, -1)
        }
        if symbol in mapper.keys():
            delta = mapper[symbol]
            self._board.push_delta(delta)

    def draw(self):
        self._board.draw()


BLOCK_SIZE = 100
GAME_SIZE = 4
player = Player(GAME_SIZE)
window = pyglet.window.Window(width=GAME_SIZE*BLOCK_SIZE,
                              height=GAME_SIZE*BLOCK_SIZE)


@window.event
def on_key_press(symbol, modifiers):
    player.on_key_press(symbol, modifiers)


def update(dt):
    window.clear()
    player.draw()


clock.schedule(update)
pyglet.app.run()
