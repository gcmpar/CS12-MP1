from __future__ import annotations
from typing import TYPE_CHECKING
from collections.abc import Callable

import pyxel

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from objects.GameObject import GameObject

from objects.Entity import Entity
from objects.Bullet import Bullet
from objects.Tank import Tank
from objects.Powerup import Powerup
from gamefiles.Modifier import Modifier

from misc.util import GameState


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
    duration = 5

    f = 0
    def text():
        nonlocal f
        powerup_text = f"The World! {duration-int(f/game.FPS)}"
        pyxel.text(pyxel.width/2-(len(powerup_text)*pyxel.FONT_WIDTH)/2,1,powerup_text,7)
    game.renderer.render_custom(text, duration=duration)

    def stop_entity(entity: Entity):
        def init(self: Modifier):
            if not isinstance(self.owner, Entity):
                return
            self.data["origOrientation"] = self.owner.orientation
            self.data["origSpeed"] = self.owner.speed

        def update(self: Modifier, frame_count: int):
            if isinstance(self.owner, Entity):
                self.owner.set_orientation(self.data["origOrientation"])
                self.owner.set_speed(0)
            if isinstance(self.owner, Tank):
                self.owner.stats["movementSpeed"].current = 0
                self.owner.stats["fireRate"].current = 0
        def destroy(self: Modifier):
            if isinstance(self.owner, Entity):
                self.owner.set_orientation(self.data["origOrientation"])
                self.owner.set_speed(self.data["origSpeed"])
            if isinstance(self.owner, Tank):
                self.owner.stats["movementSpeed"].current = self.owner.stats["movementSpeed"].base
                self.owner.stats["fireRate"].current = self.owner.stats["fireRate"].base
        def can_touch(self: Modifier, other: GameObject):
            if isinstance(other, Tank):
                if other.team == "player":
                    return
            return False

        mod = Modifier(
                game=game,
                owner=entity,
                type="TimeStop",
                priority=6969,
                init=init,
                update=update,
                destroy=destroy,
                can_touch=can_touch if isinstance(entity, Bullet) else None,
                stage_transferrable=False
            )
        record[entity] = mod
        entity.add_modifier(mod)

    def stop_conditions(entity: Entity) -> bool:
        if isinstance(entity, Tank):
            if entity.team == "player":
                return False
            
        for mod in entity.modifiers:
            if mod.type == "TimeStop":
                return False
            
        if entity in record.keys():
            return False
        
        if entity == tank:
            return False

        return True
        

    record = dict[Entity, Modifier]()
    def update(frame_count: int):
        nonlocal f
        f += 1
        if f > game.FPS * duration:
            stop()
            return
        
        for y in range(game.r):
            for x in range(game.c):
                cell = game[y, x]
                for entity in cell.get_objects():
                    if not isinstance(entity, Entity):
                        continue
                    if stop_conditions(entity):
                        stop_entity(entity)
                    
    def on_object_added(obj: GameObject):
        if not isinstance(obj, Entity):
            return
        if not stop_conditions(obj):
            return
        stop_entity(obj)
    game.onPreObjectUpdate.add_listener(update)
    game.onObjectAdded.add_listener(on_object_added)

    # self-modifier buff and tag for PlayerController use (one-bullet-only rule bypass)
    def mod_update(self: Modifier, frame_count: int):
        owner = self.owner
        if isinstance(owner, Tank):
            owner.stats["fireRate"].current = 5
    def mod_destroy(self: Modifier):
        owner = self.owner
        if isinstance(owner, Tank):
            owner.stats["fireRate"].current = owner.stats["fireRate"].base
    self_mod = Modifier(
        game=game,
        owner=tank,
        type="TimeStopBuff",
        priority=6969,
        update=mod_update,
        destroy=mod_destroy,
        stage_transferrable=False
    )
    tank.add_modifier(self_mod)


    def stop():
        game.onStateChanged.remove_listener(stop_listener)

        game.onPreObjectUpdate.remove_listener(update)
        game.onObjectAdded.remove_listener(on_object_added)
        game.renderer.stop_render_custom(text)

        for entity, mod in record.items():
            entity.remove_modifier(mod)
        tank.remove_modifier(self_mod)

    def stop_listener(state: GameState):
        stop()
    game.onStateChanged.add_listener(stop_listener)

@create(powerup_type="Mirage")
def _(game: GameField, tank: Tank):
    duration = 5

    f = 0
    def text():
        nonlocal f
        powerup_text = f"-- MIRAGE -- {duration-int(f/game.FPS)}\nFloat out of this Reality."
        pyxel.text(pyxel.width/2-(len(powerup_text)*pyxel.FONT_WIDTH)/2,1,powerup_text,7)
    game.renderer.render_custom(text, duration=duration)

    def init(self: Modifier):
        self.data["f"] = 0
    def update(self: Modifier, frame_count: int):
        nonlocal f
        self.data["f"] += 1
        f = self.data["f"]
        if self.data["f"] > game.FPS * duration:
            self.owner.remove_modifier(self)
    def can_touch(self: Modifier, other: GameObject):
        return False
    
    mod = Modifier(
        game=game,
        owner=tank,
        type="Mirage",
        priority=6969,
        init=init,
        update=update,
        can_touch=can_touch,
        stage_transferrable=False
    )
    tank.add_modifier(mod)


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