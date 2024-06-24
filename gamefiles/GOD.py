from __future__ import annotations
from typing import TYPE_CHECKING
from collections.abc import Callable
from random import choice

import pyxel

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from gamefiles.Cell import Cell

from misc.util import GameState, orientation_to_move_vector
from objects.Tank import Tank

from resources.controls import DEBUG_CONTROLS

from misc.K import K

'''
Singleton for Debug mode and cheat codes
NOTE: See resources/controls.py for debug controls

CHEAT CODES (Hold CTRL key):
    life
        - extra life, respawns player and continues game even if win/lose
    smite
        - smites all enemies present on field
    win
        - automatically win the game
    safe
        - keep yourself safe
    powerup
        - spawn a random powerup
    
        
    ???
        - kaRMa.

God
    game: GameField

    init()
    update()

'''

DEBUG_FUNCTIONS: dict[str, Callable[[GameField], None]] = {}
def create(c: str):
    def i(f: Callable[[GameField], None]):
        debounce = False
        def d_func(game: GameField):
            nonlocal debounce
            if pyxel.btn(DEBUG_CONTROLS[c]["btn"]):
                if not debounce:
                    debounce = True
                    f(game)
            else:
                debounce = False
        DEBUG_FUNCTIONS[c] = d_func
    return i

@create(c="life")
def _(game: GameField):
    stage = game.stage
    current_lives = stage.get_lives()
    
    stage.set_lives(current_lives+1)
    if stage.get_player().tank.is_destroyed():
        stage.spawn_player()

    homes = stage.get_homes()
    for home in homes:
        if home.is_destroyed():
            stage.remove_home(home)

    game.set_game_state(GameState.ONGOING)


@create(c="smite")
def _(game: GameField):
    for r in range(game.r):
        for c in range(game.c):
            cell = game[r, c]
            for obj in cell.get_objects():

                if isinstance(obj, Tank):
                    if obj.team == "enemy":
                        obj.destroy()

@create(c="win")
def _(game: GameField):
    game.set_game_state(GameState.WIN)

@create(c="safe")
def _(game: GameField):
    game.stage.get_player().tank.destroy()

@create(c="powerup")
def _(game: GameField):
    empty_cells: list[Cell] = []
    for r in range(game.r):
        for c in range(game.c):
            cell = game[r, c]
            if len(cell.get_objects()) == 0:
                empty_cells.append(cell)

    if len(empty_cells) > 0:
        chosen_cell = choice(empty_cells)
        game.powerupFactory.powerup(x=chosen_cell.x, y=chosen_cell.y, powerup_type=choice(game.powerupFactory.get_powerup_types()))


@create(c="test")
def _(game: GameField):
    game.start_stage("_TEST")







# ,..reviR derorriM
# .dlrow derorrim
@create(c="???")
def _(game: GameField):
    game.start_stage("_kaRMa")
@create(c="K")
def _(game: GameField):
    if game.stage.name == "_kaRMa":
        return
    tank = game.stage.get_player().tank
    cell = tank.get_cell()
    x_move, y_move = orientation_to_move_vector(tank.orientation)
    K(game=game, x=cell.x + x_move, y=cell.y + y_move, ori=tank.orientation)





class God:
    def __init__(self, game: GameField):
        self.game = game

    def init(self):
        pass

    def update(self):
        if self.game.get_game_state() == GameState.READY or self.game.get_game_state() == GameState.GENERATING:
            return
        
        if pyxel.btn(DEBUG_CONTROLS["debug"]["btn"]):
            for f in DEBUG_FUNCTIONS.values():
                f(self.game)