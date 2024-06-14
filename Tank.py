from typing import Literal

Direction = Literal["north", "south", "east", "west"]


'''
Tank
    x: int
        - the X position on grid

    y: int
        - the Y position on grid


    look: "north" // "south" // "east" // "west"
        - where the tank is currently facing
    
    move(dir: Direction)
        - change pos according to direction
    
    force_update(x: int, y: int, look: Direction)
        - manually update all values


'''

class Tank():
    def __init__(self, x: int = 0, y: int = 0, look: Direction = "north"):
        self.x = x
        self.y = y
        self.look = look
    
    # TODO bullet

    def move(self, dir: Direction):
        self.x += 1 if dir == "east" else -1 if dir == "west" else 0
        self.y += 1 if dir == "south" else -1 if dir == "north" else 0
        self.look = dir
    
    def force_update(self, x: int = None, y: int = None, look: int = None):
        self.x = x if not (x is None) else self.x
        self.y = y if not (y is None) else self.y
        self.look = look if not (look is None) else self.look
        