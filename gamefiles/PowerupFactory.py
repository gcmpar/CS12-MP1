from __future__ import annotations
from typing import TYPE_CHECKING, Any
from collections.abc import Callable

import pyxel

if TYPE_CHECKING:
    from gamefiles.GameField import GameField

from objects.Entity import Entity
from objects.Tank import Tank
from objects.Bullet import Bullet
from objects.Powerup import Powerup
from gamefiles.Modifier import Modifier


'''
Factory for Powerup and Modifier creation

PowerupFactory:
    - powerup(x: int, y: int, powerup_type: str)
        - selects executor functions from dictionary below based on powerup_type
        
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
        pyxel.text(pyxel.width/2-(len(powerup_text)*pyxel.FONT_WIDTH)/2,1,powerup_text,7)
    game.renderer.render_custom(text, duration=2)

@create(powerup_type="ExtraSpeed")
def _(game: GameField, tank: Tank):
    def update(self: Modifier, frame_count: int):
        if isinstance(self.owner, Tank):
            self.owner.stats["movementSpeed"].current = tank.stats["movementSpeed"].base*1.5
    def destroy(self: Modifier):
        if isinstance(self.owner, Tank):
            self.owner.stats["movementSpeed"].current = tank.stats["movementSpeed"].base
        
    mod = Modifier(
        game=game,
        owner=tank,
        type="ExtraSpeed",
        update=update,
        destroy=destroy
    )
    tank.add_modifier(mod)

    def text():
        powerup_text = "Zoooom!"
        pyxel.text(pyxel.width/2-(len(powerup_text)*pyxel.FONT_WIDTH)/2,1,powerup_text,7)
    game.renderer.render_custom(text, duration=2)

@create(powerup_type="TimeStop")
def _(game: GameField, tank: Tank):
    for mod in tank.modifiers:
        if mod.type == "TimeStop":
            def text():
                powerup_text = "Time is already stopped! Powerup failed"
                pyxel.text(pyxel.width/2-(len(powerup_text)*pyxel.FONT_WIDTH)/2,1,powerup_text,7)
            game.renderer.render_custom(text, duration=2)
            return
        
    def update(self: Modifier, frame_count: int):
        for y in range(game.r):
            for x in range(game.c):
                cell = game[y, x]
                for obj in cell.get_objects():
                    if not isinstance(obj, Entity):
                        continue
                    if obj == tank:
                        continue
                    if obj not in self.data["victims"]:
                        obj_data = dict[str, Any]()
                        
                        if isinstance(obj, Bullet):
                            obj_data["originalSpeed"] = obj.speed
                        obj_data["orientation"] = obj.orientation
                        self.data["victims"][obj] = (obj_data)
                    
                    # stat changes
                    if isinstance(obj, Tank):
                        obj.stats["movementSpeed"].current = 0
                        obj.stats["fireRate"].current = 0
                    
                    # vel changes
                    if isinstance(obj, Bullet):
                        obj.speed = 0
                    
                    obj.orientation = self.data["victims"][obj]["orientation"]
    
    def destroy(self: Modifier):
        for obj, data in self.data["victims"].items():
            if isinstance(obj, Tank):
                obj.stats["movementSpeed"].current = obj.stats["movementSpeed"].base
                obj.stats["fireRate"].current = obj.stats["fireRate"].base
            elif isinstance(obj, Bullet):
                obj.speed = data["originalSpeed"]

                    

    mod = Modifier(
        game=game,
        owner=tank,
        type="TimeStop",
        update=update,
        destroy=destroy,
        data={"victims": dict[Entity, Any]()},
        stage_transferrable=False
    )
    tank.add_modifier(mod)

    def text():
        powerup_text = "The World!"
        pyxel.text(pyxel.width/2-(len(powerup_text)*pyxel.FONT_WIDTH)/2,1,powerup_text,7)
    game.renderer.render_custom(text, duration=2)

@create(powerup_type="Mirage")
def _(game: GameField, tank: Tank):
    pass


class PowerupFactory:
    def __init__(self, game: GameField):
        self.game = game
    
    def powerup(self, x: int, y: int, powerup_type: str) -> Powerup:
        #powerup_type="TimeStop"
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