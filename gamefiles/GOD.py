from __future__ import annotations
from typing import TYPE_CHECKING
from random import choice

import pyxel

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from gamefiles.Cell import Cell

from misc.util import GameState
from objects.Tank import Tank

from resources.controls import DEBUG_CONTROLS

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

class God:
    def __init__(self, game: GameField):
        self.game = game

        self._lifeDebounce = False
        self._LTGDebounce = False
        self._powerupDebounce = False

        self._karmaDebounce = False
    
    def init(self):
        pass

    def update(self):
        if self.game.get_game_state() == GameState.READY or self.game.get_game_state() == GameState.GENERATING:
            return
        
        if pyxel.btn(DEBUG_CONTROLS["debug"]["btn"]):

            if pyxel.btn(DEBUG_CONTROLS["life"]["btn"]):
                if not self._lifeDebounce:
                    self._lifeDebounce = True

                    stage = self.game.stage
                    current_lives = stage.get_lives()
                    
                    stage.set_lives(current_lives+1)
                    if stage.get_player().tank.is_destroyed():
                        stage.spawn_player()

                    homes = stage.get_homes()
                    for home in homes:
                        if home.is_destroyed():
                            stage.remove_home(home)

                    self.game.set_game_state(GameState.ONGOING)
            else:
                self._lifeDebounce = False
            
            if pyxel.btn(DEBUG_CONTROLS["smite"]["btn"]):
                for r in range(self.game.r):
                    for c in range(self.game.c):
                        cell = self.game[r, c]
                        for obj in cell.get_objects():

                            if isinstance(obj, Tank):
                                if obj.team == "enemy":
                                    obj.destroy()

            if pyxel.btn(DEBUG_CONTROLS["win"]["btn"]):
                self.game.set_game_state(GameState.WIN)
            if pyxel.btn(DEBUG_CONTROLS["safe"]["btn"]):
                if not self._LTGDebounce:
                    self._LTGDebounce = True
                    self.game.stage.get_player().tank.destroy()
            else:
                self._LTGDebounce = False
            
            if pyxel.btn(DEBUG_CONTROLS["powerup"]["btn"]):
                if not self._powerupDebounce:
                    self._powerupDebounce = True
                    empty_cells: list[Cell] = []
                    for r in range(self.game.r):
                        for c in range(self.game.c):
                            cell = self.game[r, c]
                            if len(cell.get_objects()) == 0:
                                empty_cells.append(cell)

                    if len(empty_cells) > 0:
                        
                        chosen_cell = choice(empty_cells)
                        self.game.powerupFactory.powerup(x=chosen_cell.x, y=chosen_cell.y, powerup_type=choice(self.game.powerupFactory.get_powerup_types()))
            else:
                self._powerupDebounce = False
            
            if pyxel.btn(DEBUG_CONTROLS["???"]["btn"]):
                if not self._karmaDebounce:
                    self._karmaDebounce = True
                    
                    self.game.start_stage("kaRMa")
            else:
                self._karmaDebounce = False