from pyxelgrid import PyxelGrid
from objects.Cell import Cell
from objects.GameObject import GameObject

class Brick(GameObject):
    def __init__(self, game: PyxelGrid[Cell], x: int, y: int):
        super().__init__(game, x, y)