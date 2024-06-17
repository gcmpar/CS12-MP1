from __future__ import annotations
from typing import TYPE_CHECKING, Any, get_args

import pyxel

if TYPE_CHECKING:
    from gamefiles.GameField import GameField

from objects.Entity import Entity
from objects.Tank import Tank
from objects.Bullet import Bullet
from objects.Mirror import Mirror

from misc.util import Orientation

import assetindex

class Renderer:
    def __init__(self, game: GameField):
        self.game = game
        self._entities: dict[Entity, dict[str, Any]] = {}
    
    def update_cell(self, frame_count: int, i: int, j: int, x: int, y: int):
        cell = self.game[i, j]
        for obj in cell.get_objects():

            obj_class = type(obj)
            index = assetindex.sprites[obj_class]

            if isinstance(obj, Entity):

                if isinstance(obj, Tank):
                    index = index[get_args(Orientation).index(obj.orientation) + (4 if obj.team == "enemy" else 0)]
                elif isinstance(obj, Bullet):
                    index = index[get_args(Orientation).index(obj.orientation)]
                else:
                    index = index[0]

            elif isinstance(obj, Mirror):
                index = index[0 if obj.reflect_orientation == "northeast" else 1]
            else:
                index = index[0]

            (u_ind, v_ind) = index
            pyxel.bltm(
                x=x,
                y=y,
                w=8,
                h=8,
                tm=0,
                u=u_ind * self.game.dim,
                v=v_ind * self.game.dim,
                colkey=0
            )