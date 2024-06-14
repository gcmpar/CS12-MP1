import pyxel
import Tank

movement_controls = {
    "north": pyxel.KEY_W,
    "south": pyxel.KEY_S,
    "east": pyxel.KEY_D,
    "west": pyxel.KEY_A
}
'''
PlayerController:
    tank: Tank
        - the tank the player controls
    
    check_inputs()
        - used by the main GameField to check input presses every frame and control tank accordingly

'''

class PlayerController():
    def __init__(self, tank: Tank):
        self.tank = tank
    
    def check_inputs(self):
        for dir, key in movement_controls.items():
            if pyxel.btnp(key):
                self.tank.move(dir)