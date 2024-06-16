from pyxelgrid import PyxelGrid
from objects.Cell import Cell
from objects.GameObject import GameObject

'''
Bullet:
    vel_x: int
        - how many cells moved horizontally
    
    vel_y: int
        - how many cells moved vertically
'''

class Bullet(GameObject):
    def __init__(self, game: PyxelGrid[Cell], x: int, y: int):
        super().__init__(game, x, y)