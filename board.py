import random
from block import Block
from functools import reduce


class Board:

    def __init__(self, size=4):
        self._size = size
        self._blocks = []
        self._merged_cell = []
        self._merged_block = []
        self.reset()

    def __del__(self):
        del self._blocks
        del self._merged_cell
        del self._merged_block

    # TODO
    def win(self):
        return False

    # TODO
    def loss(self):
        return False

    def reset(self):
        self._blocks = []
        for i in range(self._size):
            self._blocks += [self._size * [None]]
        self._gen_rand()

    # 보드의 빈 칸 중 하나에서 임의로 블럭을 생성한다
    # 빈 칸이 없을 경우 아무 일도 하지 않음
    def _gen_rand(self):
        all_blocks = reduce(lambda lst, val: lst + val, self._blocks)
        available = all_blocks.count(None)
        if available == 0:
            return
        rand_val = random.randrange(2, 5, 2)
        count = random.randrange(1, available + 1)
        for i in range(self._size):
            for j in range(self._size):
                if self._blocks[i][j] is None:
                    count -= 1
                if count == 0:
                    self._blocks[i][j] = Block(i, j, rand_val)
                    return

    def _merge_block(self, from_i, from_j, to_i, to_j):
        self._blocks[from_i][from_j].moveto(to_i, to_j)
        self._blocks[to_i][to_j].upgrade()
        self._merged_cell += [(to_i, to_j)]
        self._merged_block += [self._blocks[from_i][from_j]]
        self._blocks[from_i][from_j] = None

    def _move_block(self, from_i, from_j, to_i, to_j):
        self._blocks[from_i][from_j].moveto(to_i, to_j)
        self._blocks[to_i][to_j] = self._blocks[from_i][from_j]
        self._blocks[from_i][from_j] = None

    def _push_block(self, i, j, delta):
        di, dj = delta
        block = self._blocks[i][j]
        if block is None:
            return
        while True:
            i = i + di
            j = j + dj
            if i not in range(self._size) or j not in range(self._size):
                return
            if self._blocks[i][j] is not None:
                if self._blocks[i][j] == block and (i, j) not in self._merged_cell:
                    self._merge_block(i-di, j-dj, i, j)
                return
            self._move_block(i-di, j-dj, i, j)
            self._moved = True

    # 주어진 방향으로 보드 전체의 숫자를 민다
    def push_delta(self, delta):
        di, dj = delta
        self._moved = False
        self._merged_cell = []
        self._merged_block = []
        if di != 0:
            for i in list(range(self._size))[::-di]:
                for j in range(self._size):
                    self._push_block(i, j, delta)
        if dj != 0:
            for j in list(range(self._size))[::-dj]:
                for i in range(self._size):
                    self._push_block(i, j, delta)
        if self._moved:
            self._gen_rand()

    def draw(self):
        for block in self._merged_block:
            block.draw()
        all_blocks = reduce(lambda lst, val: lst + val, self._blocks)
        for block in all_blocks:
            if block is not None:
                    block.draw()