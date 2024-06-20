from __future__ import annotations
from typing import TYPE_CHECKING

import pyxel

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from objects.GameObject import GameObject

from objects.Bullet import Bullet
from objects.Tank import Tank

class SoundManager:
    def __init__(self, game: GameField):
        self.game = game
    
    def init(self):
        def initialize(obj: GameObject):
            if isinstance(obj, Bullet):
                def onExplode():
                    pyxel.play(0, pyxel.sounds[1])
                obj.onCollision.add_listener(lambda obj: onExplode())
                obj.onOutOfBounds.add_listener(onExplode)

            elif isinstance(obj, Tank):

                def onDestroy():
                    pyxel.play(0, pyxel.sounds[2])
                obj.onDestroy.add_listener(onDestroy)

        self.game.onObjectAdded.add_listener(initialize)

    def update(self, frame_count: int):
        pass