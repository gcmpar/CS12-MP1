import pyxel
from pyxelgrid import PyxelGrid

from objects.util import Direction, clamp

'''
Tank
    x: int
        - the X position on grid

    y: int
        - the Y position on grid

    direction: "north" // "south" // "east" // "west"
        - where the tank is currently facing
    
    speed: int
    - how many cells the tank can move per second

    
    move(dir: Direction) -> bool
        - change pos according to direction
        - limited by speed
        - returns True if moved to cell successfully


'''

class Tank():
    def __init__(self, game = PyxelGrid[int], x: int = 0, y: int = 0, dir: Direction = "east"):
        self._game = game
        self._last_move_frame = 0

        self.x = x
        self.y = y
        self.direction = dir
        self.speed = 5
    
    # TODO bullet

    def move(self, dir: Direction) -> bool:
        # movement cap
        if pyxel.frame_count < (self._last_move_frame + (self._game.FPS / self.speed)):
            return False
        self._last_move_frame = pyxel.frame_count
        self.direction = dir


        x_move = 1 if dir == "east" else -1 if dir == "west" else 0
        y_move = 1 if dir == "south" else -1 if dir == "north" else 0
        
        # sanity check
        new_x = clamp(self.x + x_move, 0, self._game.c-1)
        new_y = clamp(self.y + y_move, 0, self._game.c-1)
        if self.x == new_x and self.y == new_y:
            return False



        # update
        self.x = new_x
        self.y = new_y
        return True
        