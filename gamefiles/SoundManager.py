from __future__ import annotations
from typing import TYPE_CHECKING

import pyxel

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from objects.GameObject import GameObject

from objects.Bullet import Bullet
from objects.Tank import Tank

from misc.util import GameState


'''
Singleton for sounds

SoundManager
    init()
        - called on GameField initialization
        - connects to signals for:
            - bullet firing
            - bullet exploding
            - tank destruction
'''

class SoundManager:
    def __init__(self, game: GameField):
        self.game = game
    
    def init(self):
        def initialize(obj: GameObject):
            if self.game.get_game_state() == GameState.GENERATING:
                return
            if isinstance(obj, Bullet) or isinstance(obj, Tank):
                def on_explode():
                    if self.game.get_game_state() == GameState.GENERATING:
                        return
                    pyxel.play(0, pyxel.sounds[1 if isinstance(obj, Bullet) else 3])
                obj.onDestroy.add_listener(on_explode)

                if isinstance(obj, Bullet):
                    pyxel.play(0,pyxel.sounds[0])

        self.game.onObjectAdded.add_listener(initialize)

    def update(self, frame_count: int):
        pass