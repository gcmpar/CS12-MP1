from __future__ import annotations
from typing import TYPE_CHECKING, Any
from collections.abc import Callable
from random import choice, randint

import pyxel

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from gamefiles.StageFile import Stage
    from gamefiles.Cell import Cell
    from gamefiles.EnemyController import EnemyController

from objects.Mirror import Mirror
from objects.Karma import Karma

from resources.controls import DEBUG_CONTROLS
from misc.util import orientation_to_move_vector
from misc.K import K

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
        restartText
        restartTextColor

    loseText
        - will default to detecting if home cell was destroyed/if player died
    loseTextColor

FUNCTIONS (optional):
    init
    update
    cleanup

---------------------------------
FORMAT:
NOTE: data is intended for passing around variables instead of using the current scope
@create(name={STAGE NAME})
def _():
    def init(game: GameField, stage: Stage, data: dict[str, Any]):
        ...

    def update(game: GameField, stage: Stage, data: dict[str, Any], frame_count: int):
        ...

    def cleanup(game: GameField, stage: Stage, data: dict[str, Any])
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
    settings: dict[str, Any] = {
        "lives": 1,
        "enemySpawns": 13,

        "winText": "- The Limitless Garden. -",
        "winTextColor": 8,

        "nextText": "Suffer.",
        "loseText": "- The Limitless Garden. -",
        "restartText": "Escape."
    }

    def init(game: GameField, stage: Stage, data: dict[str, Any]):
        data["lastSpawnFrame"] = -6969
        data["spawnInterval"] = 7
        data["eventCleanups"] = list[Callable[[], None]]()
        data["karmaDebounce"] = False
        data["kUses"] = 3


        # powerup and karma spawn
        def spawn(_: EnemyController):
            enemy_count = stage.get_total_enemy_count()
            max_enemies = stage.get_max_enemies()
            
            if max_enemies > 1 and enemy_count >= 1 and enemy_count <= max_enemies * 0.75:
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
                
                karma_count = 1
                if max_enemies < 0.35:
                    karma_count = 2
                mirrors: list[Mirror] = []
                for r in range(game.r):
                    for c in range(game.c):
                        cell = game[r, c]
                        for obj in cell.get_objects():
                            if not isinstance(obj, Mirror):
                                continue
                            if r == 0 or r == game.r-1:
                                continue
                            if c == 0 or c == game.c-1:
                                continue
                            mirrors.append(obj)
                if len(mirrors) > 0:
                    for _ in range(karma_count):
                        mirror = choice(mirrors)
                        cell = mirror.get_cell()
                        mirror.destroy()
                        Karma(game=game, x=cell.x, y=cell.y)
        
        stage.onEnemyRemoved.add_listener(spawn)
        def remove_listener():
            stage.onEnemyRemoved.remove_listener(spawn)
        data["eventCleanups"].append(remove_listener)

    def update(game: GameField, stage: Stage, data: dict[str, Any], frame_count: int):
        enemy_spawns = stage.get_enemy_spawns()
        l = len(enemy_spawns) 
        if l > 0:
            if frame_count > (data["lastSpawnFrame"] + (game.FPS * data["spawnInterval"])):
                data["lastSpawnFrame"] = frame_count

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

        if data["kUses"] > 0:
            if pyxel.btn(DEBUG_CONTROLS["K"]["btn"]):
                if not data["karmaDebounce"]:
                    data["karmaDebounce"] = True
                    data["kUses"] -= 1

                    tank = game.stage.get_player().tank
                    cell = tank.get_cell()
                    x_move, y_move = orientation_to_move_vector(tank.orientation)
                    K(game=game, x=cell.x + x_move, y=cell.y + y_move, ori=tank.orientation)
            else:
                data["karmaDebounce"] = False

        game.renderer.display_text(1,1+pyxel.FONT_HEIGHT*3,f"K{data["kUses"]}",3)
        

    def cleanup(game: GameField, stage: Stage, data: dict[str, Any]):
        [f() for f in data["eventCleanups"]]

    settings["init"] = init
    settings["update"] = update
    settings["cleanup"] = cleanup
    return settings


@create(name="_empty")
def _():
    def init(game: GameField, stage: Stage, data: dict[str, Any]):
        pass
    def update(game: GameField, stage: Stage, data: dict[str, Any], frame_count: int):
        pass
    def cleanup(game: GameField, stage: Stage, data: dict[str, Any]):
        pass
    return {
        "lives": 1,
        "enemySpawns": 0,

        "init": init,
        "update": update,
        "cleanup": cleanup,
    }
@create(name="_TEST")
def _():
    def init(game: GameField, stage: Stage, data: dict[str, Any]):
        pass
    def update(game: GameField, stage: Stage, data: dict[str, Any], frame_count: int):
        pass
    def cleanup(game: GameField, stage: Stage, data: dict[str, Any]):
        pass
    return {
        "lives": 999,
        "enemySpawns": 999,
        "init": init,
        "update": update,
        "cleanup": cleanup,
    }









for d in STAGE_SETTINGS.values():
    # SETTINGS
    d.setdefault("winText", "STAGE FINISHED")
    d.setdefault("winTextColor", 12)

    d.setdefault("nextText", "Advance")
    d.setdefault("nextTextColor", 11)

    d.setdefault("loseTextColor", 8)

    d.setdefault("restartText", "Restart")
    d.setdefault("restartTextColor", 11)


    # FUNCTIONS
    def scope():
        def default_init(game: GameField, stage: Stage, data: dict[str, Any]):
            data["lastSpawnFrame"] = -6969
            data["spawnInterval"] = 3.5
            data["eventCleanups"] = list[Callable[[], None]]()

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
            data["eventCleanups"].append(remove_listener)

        def default_update(game: GameField, stage: Stage, data: dict[str, Any], frame_count: int):
            enemy_spawns = stage.get_enemy_spawns()
            l = len(enemy_spawns) 
            if l > 0:
                if frame_count > (data["lastSpawnFrame"] + (game.FPS * data["spawnInterval"])):
                    data["lastSpawnFrame"] = frame_count
                    stage.spawn_enemy_delayed(spawn_index=randint(0, l-1), tank_type=choice(game.tankFactory.get_tank_types()))

        def default_cleanup(game: GameField, stage: Stage, data: dict[str, Any]):
            [f() for f in data["eventCleanups"]]

        d.setdefault("init", default_init)
        d.setdefault("update", default_update)
        d.setdefault("cleanup", default_cleanup)
    scope()