from __future__ import annotations
from typing import TYPE_CHECKING, Any
from collections.abc import Callable
from random import choice, randint

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from gamefiles.StageFile import Stage
    from gamefiles.Cell import Cell
    from gamefiles.EnemyController import EnemyController
'''
SETTINGS:
    REQUIRED:
        lives
        enemySpawns

    OPTIONAL:
        winText
        winTextColor
        nextText
        nextTextColor

    loseText
        - will default to detecting if home cell was destroyed/if player died
    loseTextColor

FUNCTIONS (optional):
    init()
    update()
    cleanup()

---------------------------------
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
        "lives": ?,
        "enemySpawns": ?
        ...
        ...

        "init": init,
        "update": update,
        "cleanup": cleanup,
    }

NOTE: can use this scope for any variables needed to be passed around
'''


STAGE_SETTINGS: dict[str, dict[str, Any]] = {}
def create(name: str):
    def i(f: Callable[[], dict[str, Any]]):
        STAGE_SETTINGS[name] = f()
    return i

@create(name="1")
def _():
    return {
        "lives": 2,
        "enemySpawns": 1,

        "winText": "VICTORY",
    }

@create(name="2")
def _():
    return {
        "lives": 2,
        "enemySpawns": 3,

        "winText": "VICTORY",

    }

@create(name="3")
def _():
    return {
        "lives": 2,
        "enemySpawns": 5,

        "winText": "GAME WON!!! :D",
        "winTextColor": 10,

        "nextText": "Repeat",
    }





@create(name="_kaRMa")
def _():
    data: dict[str, Any] = {
        "lives": 1,
        "enemySpawns": 13,

        "winText": "- The Limitless Garden. -",
        "winTextColor": 8,

        "nextText": "Suffer.",

        "loseText": "- The Limitless Garden. -",
    }



    last_spawn_frame = -6969
    spawn_interval = 7
    event_cleanups: list[Callable[[], None]] = []
    def init(game: GameField, stage: Stage):
        
        # powerup spawn
        def spawn_powerup(_: EnemyController):
            enemy_count = stage.get_total_enemy_count()
            max_enemies = stage.get_max_enemies()
            if max_enemies > 1 and enemy_count >= 1 and enemy_count <= max_enemies / 2:

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
    
    data["init"] = init
    data["update"] = update
    data["cleanup"] = cleanup
    return data


@create(name="_empty")
def _():
    return {
        "lives": 1,
        "enemySpawns": 0,
    }
@create(name="_TEST")
def _():
    return {
        "lives": 999,
        "enemySpawns": 999,
    }









for d in STAGE_SETTINGS.values():
    # SETTINGS
    d.setdefault("winText", "STAGE FINISHED")
    d.setdefault("winTextColor", 12)

    d.setdefault("nextText", "Advance")
    d.setdefault("nextTextColor", 11)

    d.setdefault("loseTextColor", 8)


    # FUNCTIONS
    def scope():
        last_spawn_frame = -6969
        spawn_interval = 3.5
        event_cleanups: list[Callable[[], None]] = []
        def default_init(game: GameField, stage: Stage):
            
            # powerup spawn
            def spawn_powerup(_: EnemyController):
                enemy_count = stage.get_total_enemy_count()
                max_enemies = stage.get_max_enemies()
                if max_enemies > 1 and enemy_count >= 1 and enemy_count <= max_enemies / 2:

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