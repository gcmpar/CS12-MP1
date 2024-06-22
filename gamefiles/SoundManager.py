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
            if isinstance(obj, Bullet):
                def on_explode():
                    pyxel.play(0, pyxel.sounds[1])
                def on_collision(other: GameObject):
                    on_explode()
                obj.onCollision.add_listener(on_collision)
                obj.onOutOfBounds.add_listener(on_explode)

                def stop(state: GameState):
                    self.game.onStateChanged.remove_listener(stop)

                    obj.onCollision.remove_listener(on_collision)
                    obj.onOutOfBounds.remove_listener(on_explode)

                self.game.onStateChanged.add_listener(stop)

                pyxel.play(0,pyxel.sounds[0])

            elif isinstance(obj, Tank):

                def on_destroy():
                    pyxel.play(0, pyxel.sounds[3])
                obj.onDestroy.add_listener(on_destroy)

                def stop(state: GameState):
                    self.game.onStateChanged.remove_listener(stop)
                    obj.onDestroy.remove_listener(on_destroy)

                self.game.onStateChanged.add_listener(stop)

        self.game.onObjectAdded.add_listener(initialize)

    def update(self, frame_count: int):
        pass