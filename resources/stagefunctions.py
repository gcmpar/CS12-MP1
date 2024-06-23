from __future__ import annotations
from typing import TYPE_CHECKING
from collections.abc import Callable
from random import choice, randint

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from gamefiles.StageFile import Stage
    from gamefiles.Cell import Cell
    from gamefiles.EnemyController import EnemyController


'''
FORMAT:
@create(name={STAGE NAME})
def _():
    def init(game: GameField, stage: Stage):
        ...

    def update(game: GameField, stage: Stage, frame_count: int):
        ...

    def cleanup(game: GameField, stage: Stage)
        ...

    return {
        "init": init,
        "update": update,
        "cleanup": cleanup,
    }

NOTE: can use this scope for any variables needed to be passed around
NOTE: all functions are optional, the decorated function can return None if you wish to use all default functions

'''

STAGE_FUNCTIONS: dict[str, dict[str, Callable[..., None]]] = {}
def create(name: str):
    def i(f: Callable[[], dict[str, Callable[..., None]] | None]):
        v = f()
        STAGE_FUNCTIONS[name] = v if v is not None else dict[str, Callable[..., None]]()
    return i


@create(name="1")
def _():
    ...

@create(name="2")
def _():
    ...

@create(name="3")
def _():
    ...







@create(name="_kaRMa")
def _():
    last_spawn_frame = -6969
    spawn_interval = 3.5
    event_cleanups: list[Callable[[], None]] = []
    def init(game: GameField, stage: Stage):
        
        # powerup spawn
        def spawn_powerup(_: EnemyController):
            if remove_listener in event_cleanups:
                event_cleanups.remove(remove_listener)

            enemy_count = stage.get_total_enemy_count()
            if stage.get_max_enemies() > 1 and enemy_count >= 1 and enemy_count <= stage.get_max_enemies() / 2:

                empty_cells: list[Cell] = []
                for r in range(game.r):
                    for c in range(game.c):
                        cell = game[r, c]
                        if len(cell.get_objects()) == 0:
                            empty_cells.append(cell)

                if len(empty_cells) > 0:
                    
                    chosen_cell = choice(empty_cells)
                    game.powerupFactory.powerup(
                        x=chosen_cell.x,
                        y=chosen_cell.y,
                        powerup_type=choice(game.powerupFactory.get_powerup_types()))
        
        stage.onEnemyRemoved.add_listener(spawn_powerup)
        def remove_listener():
            stage.onEnemyRemoved.remove_listener(spawn_powerup)
        event_cleanups.append(remove_listener)

    def update(game: GameField, stage: Stage, frame_count: int):
        nonlocal last_spawn_frame

        enemy_spawns = stage.get_enemy_spawns()
        l = len(enemy_spawns) 
        if l > 0:
            if frame_count > (last_spawn_frame + (game.FPS * spawn_interval)):
                last_spawn_frame = frame_count

                enemy_count = stage.get_total_enemy_count()
                max_enemies = stage.get_max_enemies()
                if enemy_count > max_enemies * 0.75:
                    tank_type = "Normal"
                elif enemy_count > max_enemies * 0.4:
                    tank_type = "Armored"
                else:
                    # good luck. :]
                    tank_type = "Light"
                stage.spawn_enemy_delayed(spawn_index=randint(0, l-1), tank_type=tank_type)

    def cleanup(game: GameField, stage: Stage):
        [f() for f in event_cleanups]

    return {
        "init": init,
        "update": update,
        "cleanup": cleanup,
    }



@create(name="_empty")
def _():
    ...
@create(name="_TEST")
def _():
    ...





# DEFAULT FUNCTIONS
# Powerups start spawning for each enemy kill when there are less than half of the maximum number of enemies from the start of the stage.
# Enemies also spawn periodically.
for d in STAGE_FUNCTIONS.values():
    def scope():
        last_spawn_frame = -6969
        spawn_interval = 3.5
        event_cleanups: list[Callable[[], None]] = []
        def default_init(game: GameField, stage: Stage):
            
            # powerup spawn
            def spawn_powerup(_: EnemyController):
                if remove_listener in event_cleanups:
                    event_cleanups.remove(remove_listener)

                enemy_count = stage.get_total_enemy_count()
                if stage.get_max_enemies() > 1 and enemy_count >= 1 and enemy_count <= stage.get_max_enemies() / 2:

                    empty_cells: list[Cell] = []
                    for r in range(game.r):
                        for c in range(game.c):
                            cell = game[r, c]
                            if len(cell.get_objects()) == 0:
                                empty_cells.append(cell)

                    if len(empty_cells) > 0:
                        
                        chosen_cell = choice(empty_cells)
                        game.powerupFactory.powerup(
                            x=chosen_cell.x,
                            y=chosen_cell.y,
                            powerup_type=choice(game.powerupFactory.get_powerup_types()))
            
            stage.onEnemyRemoved.add_listener(spawn_powerup)
            def remove_listener():
                stage.onEnemyRemoved.remove_listener(spawn_powerup)
            event_cleanups.append(remove_listener)

        def default_update(game: GameField, stage: Stage, frame_count: int):
            nonlocal last_spawn_frame

            enemy_spawns = stage.get_enemy_spawns()
            l = len(enemy_spawns) 
            if l > 0:
                if frame_count > (last_spawn_frame + (game.FPS * spawn_interval)):
                    last_spawn_frame = frame_count
                    stage.spawn_enemy_delayed(spawn_index=randint(0, l-1), tank_type=choice(game.tankFactory.get_tank_types()))

        def default_cleanup(game: GameField, stage: Stage):
            [f() for f in event_cleanups]

        d.setdefault("init", default_init)
        d.setdefault("update", default_update)
        d.setdefault("cleanup", default_cleanup)
    scope()