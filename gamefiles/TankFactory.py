from __future__ import annotations
from typing import TYPE_CHECKING, Any
from collections.abc import Callable

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from misc.util import Team
    from objects.GameObject import GameObject

from objects.Tank import Tank
from objects.Bullet import Bullet
from gamefiles.Modifier import Modifier

'''
Factory for Tank creation

TankFactory:
    - tank(x: int, y: int, team: Team, tank_type: str)
        - selects stats from dictionary below based on tank_type
        
    - get_tank_types() -> list[str]
'''

'''
REQIUIRED:
    stats:
        health
        movementSpeed
        fireRate
OPTIONAL:
    init()

---------------------------------
FORMAT:
@create(name={TANK TYPE})
def _():
    return {
        "stats": {
            "health": ?,
            "movementSpeed": ?,
            "fireRate": ?,
            "bulletSpeed": ?,
        }
        "init": Callable[[GameField, Tank], None],
    }
'''

TANK_TYPES: dict[str, dict[str, Any]] = {}
def create(tank_type: str):
    def i(f: Callable[[], dict[str, Any]]):
        TANK_TYPES[tank_type] = f()
    return i

@create(tank_type="Normal")
def _():
    data = {
        "stats": {
            "health": 1,
            "movementSpeed": 5,
            "fireRate": 1,
            "bulletSpeed": 15,
        }
    }
    return data


@create(tank_type="Armored")
def _():
    data = {
        "stats": {
            "health": 5,
            "movementSpeed": 3,
            "fireRate": 0.5,
            "bulletSpeed": 15,
        }
    }
    return data

@create(tank_type="Light")
def _():
    data: dict[str, Any] = {
        "stats": {
            "health": 2,
            "movementSpeed": 8,
            "fireRate": 3,
            "bulletSpeed": 44,
        }
    }
    def init(game: GameField, tank: Tank):
        # Yeah!
        def mid_air(bullet: Bullet):
            def init(self: Modifier):
                owner = self.owner
                assert isinstance(owner, Bullet)

                self.data["origSpeed"] = owner.speed
                self.data["frames"] = 0
                owner.speed = self.game.FPS / 8

            def update(self: Modifier, frame_count: int):
                self.data["frames"] += 1
                if self.data["frames"] > self.game.FPS * 0.65:
                    self.owner.remove_modifier(self)
                    return

                owner = self.owner
                assert isinstance(owner, Bullet)
                owner.speed = self.game.FPS / 8

            def destroy(self: Modifier):
                owner = self.owner
                assert isinstance(owner, Bullet)
                owner.speed = self.data["origSpeed"]

            def can_collide(self: Modifier, other: GameObject):
                owner = self.owner
                assert isinstance(owner, Bullet)

                if isinstance(other, Bullet):
                    if other.owner.team == owner.owner.team:
                        if other.has_modifier_type("_midair"):
                            return False
                return owner.can_collide(other)

            mod = Modifier(
                game=game,
                type="_midair",
                priority=69,
                init=init,
                update=update,
                destroy=destroy,
                can_collide=can_collide,
                stage_transferrable=False
            )
            bullet.add_modifier(mod)
        tank.onBulletFired.add_listener(mid_air)

    data["init"] = init
    return data




for d in TANK_TYPES.values():
    def init(game: GameField, tank: Tank):
        pass
    d.setdefault("init", init)

class TankFactory:
    def __init__(self, game: GameField):
        self.game = game
    
    def tank(self, x: int, y: int,
             team: Team, tank_type: str,
             pre_added: Callable[[GameObject], bool] | None = None) -> Tank:
        
        data = TANK_TYPES[tank_type]
        stats = data["stats"]
        
        tank = Tank(game=self.game, x=x, y=y, pre_added = pre_added, team=team,tank_type=tank_type,
                    
                    health=stats["health"],
                    movement_speed=stats["movementSpeed"],
                    fire_rate=stats["fireRate"],
                    bullet_speed=stats["bulletSpeed"]
                    
                    )
        data["init"](self.game, tank)

        return tank

    def get_tank_types(self) -> list[str]:
        return list(TANK_TYPES)