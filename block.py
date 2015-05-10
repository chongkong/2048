import pyglet
from pyglet.gl import *
from functools import reduce


SIZE = 100
PADDING = 10
ROUNDING_RADIUS = 5


class Block:

    def __init__(self, i, j, value):
        self._pos = self._coordinate(i, j)
        self._moveto = None
        self._label = _BlockLabel(self._pos, value)
        self._sprite = _BlockSprite(self._pos, value)
        self.set_value(value)

    def __del__(self):
        del self._pos
        del self._value
        del self._moveto
        del self._label
        del self._sprite

    def __eq__(self, other):
        return False if other is None else self._value == other._value

    def set_value(self, value):
        self._value = value
        self._label.set_value(value)
        self._sprite.set_value(value)

    @staticmethod
    def _coordinate(i, j):
        return (i + 0.5) * SIZE, (j + 0.5) * SIZE

    def moveto(self, i, j):
        self._moveto = self._coordinate(i, j)

    def upgrade(self):
        self.set_value(self._value * 2)

    def draw(self):
        self._update_pos()
        self._sprite.draw()
        self._label.draw()

    def _update_pos(self):
        self._tween()
        self._sprite.set_pos(self._pos)
        self._label.set_pos(self._pos)

    def _tween(self):
        if self._moveto is None:
            return
        (x, y) = self._pos
        (p, q) = self._moveto
        if abs(x-p) + abs(y-q) < 1:
            self._pos = (p, q)
            self._moveto = None
        else:
            self._pos = (x + p) / 2, (y + q) / 2


class _BlockColor:

    sprite_default = (255, 255, 255, 255)
    label_default = (0, 0, 0, 255)
    sprite_mapper = {
        2: (0xee, 0xe4, 0xda, 0xff),
        4: (0xed, 0xe0, 0xc8, 0xff),
        8: (0xf2, 0xb1, 0x79, 0xff),
        16: (0xf5, 0x95, 0x63, 0xff),
        32: (0xf6, 0x7c, 0x5f, 0xff),
        64: (0xf6, 0x5e, 0x3b, 0xff),
        128: (0xed, 0xcf, 0x72, 0xff),
        256: (0xed, 0xcc, 0x61, 0xff),
        512: (0xed, 0xc8, 0x50, 0xff),
        1024: (0xed, 0xc5, 0x3f, 0xff),
        2048: (0xed, 0xc2, 0x2e, 0xff),
        4096: (0x3c, 0x3a, 0x32, 0xff)
    }

    @staticmethod
    def sprite_color(value):
        if value > 4096:
            value = 4096
        return _BlockColor.sprite_mapper[value]

    @staticmethod
    def label_color(value):
        if value <= 4:
            return (0, 0, 0, 255)
        else:
            return (255, 255, 255, 255)


class _BlockLabel:

    def __init__(self, pos, value):
        self._label = pyglet.text.Label(width=SIZE-2*PADDING, font_size=40,
                                        anchor_x='center', anchor_y='center',
                                        bold=True)
        self.set_pos(pos)
        self.set_value(value)

    def __del__(self):
        del self._label

    def set_pos(self, pos):
        (fx, fy) = pos
        self._label.x, self._label.y = int(fx), int(fy)

    def set_value(self, value):
        if value >= 100:
            self._label.font_size = 30
        if value >= 1000:
            self._label.font_size = 25
        self._label.text = str(value)
        self._label.color = _BlockColor.label_color(value)

    def draw(self):
        self._label.draw()


class _BlockSprite:

    def __init__(self, pos, value):
        self.set_pos(pos)
        self.set_value(value)

    def __del__(self):
        del self._pos
        del self._points
        del self._color

    def _build_points(self):
        x, y = self._pos
        d = (SIZE - PADDING) / 2
        self._points = [(x-d, y-d), (x+d, y-d), (x+d, y+d), (x-d, y+d)]

    def set_pos(self, pos):
        self._pos = pos
        self._build_points()

    def set_value(self, value):
        self._color = _BlockColor.sprite_color(value)

    def draw(self):
        (r, g, b, a) = self._color
        glColor3f(r/255, g/255, b/255)
        glBegin(GL_QUADS)
        for (x, y) in self._points:
            glVertex2f(x, y)
        glEnd()

        '''
        points_flatten = reduce(lambda _lst, tpl: _lst + list(tpl), self._points, [])
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                             ('v2f', points_flatten))
        '''