from __future__ import annotations
from typing import TYPE_CHECKING
from collections.abc import Callable

import pyxel

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from objects.Tank import Tank

from objects.Powerup import Powerup
from gamefiles.Modifier import Modifier


'''
Factory for Powerup and Modifier creation

PowerupFactory:
    - powerup(x: int, y: int, powerup_type: str)
        - selects executor functions from dictionary above based on powerup_type
        
    - get_powerup_types() -> list[str]
'''


powerups: dict[str, Callable[[GameField, Tank], None]] = {}
def create(powerup_type: str):
    def i(f: Callable[[GameField, Tank], None]):
        powerups[powerup_type] = f
        return f
    return i


# POWERUPS
@create(powerup_type="ExtraLife")
def _(game: GameField, tank: Tank):
    game.stage.set_lives(game.stage.get_lives() + 1)
    def text():
        powerup_text = "Extra Life!"
        pyxel.text(pyxel.width/2-(len(powerup_text)*pyxel.FONT_WIDTH),1,powerup_text,7)
    game.renderer.render_custom(text, duration=2)

@create(powerup_type="ExtraSpeed")
def _(game: GameField, tank: Tank):
    def update(frame_count: int):
        tank.stats["movementSpeed"].current = tank.stats["movementSpeed"].base*1.5
    def destroy():
        tank.stats["movementSpeed"].current = tank.stats["movementSpeed"].base
        
    mod = Modifier(
        game=game,
        owner=tank,
        update=update,
        destroy=destroy
    )
    tank.add_modifier(mod)

    def text():
        powerup_text = "Zoooom!"
        pyxel.text(pyxel.width/2-(len(powerup_text)*pyxel.FONT_WIDTH),1,powerup_text,7)
    game.renderer.render_custom(text, duration=2)

class PowerupFactory:
    def __init__(self, game: GameField):
        self.game = game
    
    def powerup(self, x: int, y: int, powerup_type: str) -> Powerup:
        def execute(tank: Tank):
            powerups[powerup_type](self.game, tank)
        return Powerup(
            game=self.game,
            x=x,
            y=y,
            type=powerup_type,
            execute=execute
        )
        
    def get_powerup_types(self) -> list[str]:
        return list(powerups.keys())