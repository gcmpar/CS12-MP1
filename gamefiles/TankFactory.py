from __future__ import annotations
from typing import TYPE_CHECKING
from collections.abc import Callable

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from misc.util import Team
    from objects.GameObject import GameObject

from objects.Tank import Tank

'''
Factory for Tank creation

TankFactory:
    - tank(x: int, y: int, team: Team, tank_type: str)
        - selects stats from dictionary below based on tank_type
        
    - get_tank_types() -> list[str]
'''

TANK_TYPES: dict[str, dict[str, float]] = {
    "Normal": {
        "health": 1,
        "movementSpeed": 5,
        "fireRate": 1,
    },
    "Armored": {
        "health": 5,
        "movementSpeed": 3,
        "fireRate": 0.5,
    },
    "Light": {
        "health": 2,
        "movementSpeed": 8,
        "fireRate": 3
    }
}

class TankFactory:
    def __init__(self, game: GameField):
        self.game = game
    
    def tank(self, x: int, y: int,
             team: Team, tank_type: str,
             pre_added: Callable[[GameObject], bool] | None = None) -> Tank:
        stats = TANK_TYPES[tank_type]
        return Tank(game=self.game, x=x, y=y, pre_added = pre_added, team=team,tank_type=tank_type,
                    
                    health=stats["health"],
                    movement_speed=stats["movementSpeed"],
                    fire_rate=stats["fireRate"]
                    
                    )

    def get_tank_types(self) -> list[str]:
        return list(TANK_TYPES)