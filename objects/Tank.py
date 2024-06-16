import pyxel
from pyxelgrid import PyxelGrid

from objects.GameObject import GameObject
from objects.util import Direction, clamp

'''
Tank
    direction: "north" // "south" // "east" // "west"
        - where the tank is currently facing
    
    speed: int
    - how many cells the tank can move per second

    
    move(dir: Direction) -> bool
        - change pos according to direction
        - limited by speed
        - returns True if moved to cell successfully


'''

class Tank(GameObject):
    from objects.Cell import Cell

    def __init__(self, game: PyxelGrid[Cell], x: int, y: int, dir: Direction = "east"):
        super().__init__(game, x, y)
        
        self._last_move_frame = 0
        self.direction = dir
        self.speed = 5

    def move(self, dir: Direction) -> bool:
        # movement cap
        if pyxel.frame_count < (self._last_move_frame + (self._game.FPS / self.speed)):
            return False
        self._last_move_frame = pyxel.frame_count
        self.direction = dir


        x_move = 1 if dir == "east" else -1 if dir == "west" else 0
        y_move = 1 if dir == "south" else -1 if dir == "north" else 0
        
        # sanity check
        current_cell = self.get_cell()
        new_x = clamp(current_cell.x + x_move, 0, self._game.c-1)
        new_y = clamp(current_cell.y + y_move, 0, self._game.c-1)
        if current_cell.x == new_x and current_cell.y == new_y:
            return False



        # update
        return self.move_to(new_x, new_y)

    def fire(self):
        pass
        