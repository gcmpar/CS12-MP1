from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from misc.util import Team
from objects.Tank import Tank

tank_stats: dict[str, dict[str, float]]  = {
    "normal": {
        "health": 1,
        "movementSpeed": 5,
        "fireRate": 1,
    },
    "armored": {
        "health": 5,
        "movementSpeed": 3,
        "fireRate": 0.5,
    },
    "light": {
        "health": 2,
        "movementSpeed": 8,
        "fireRate": 3
    }
}

class TankFactory:
    def __init__(self, game: GameField):
        self.game = game
    
    def tank(self, x: int, y: int, team: Team, tank_type: str) -> Tank:
        stats = tank_stats[tank_type]
        return Tank(game=self.game, x=x, y=y, team=team,tank_type=tank_type,
                    
                    health=stats["health"],
                    movement_speed=stats["movementSpeed"],
                    fire_rate=stats["fireRate"]
                    
                    )

    def get_tank_types(self) -> list[str]:
        return list(tank_stats.keys())