from __future__ import annotations
from typing import TYPE_CHECKING, Any, get_args

import pyxel

if TYPE_CHECKING:
    from gamefiles.GameField import GameField

from objects.Entity import Entity
from objects.Tank import Tank
from objects.Bullet import Bullet
from objects.Mirror import Mirror
from objects.Brick import Brick

from misc.util import Orientation, GameState

import resources.assetindex as assetindex

class Renderer:
    def __init__(self, game: GameField):
        self.game = game
        self._entities: dict[Entity, dict[str, Any]] = {}
    
    def init(self):
        pass

    def draw_cell(self, frame_count: int, i: int, j: int, x: int, y: int):
        if self.game.currentGameState == GameState.READY:
            return
        
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
                index = index[0 if obj.reflectOrientation == "northeast" else 1]
            elif isinstance(obj, Brick):
                index = index[0 if not obj.cracked else 1]
            else:
                index = index[0]

            # Old 8x8 sprite rendering
            # (u_ind, v_ind) = index
            # pyxel.bltm(
            #     x=x,
            #     y=y,
            #     w=8,
            #     h=8,
            #     tm=0,
            #     u=u_ind * self.game.dim,
            #     v=v_ind * self.game.dim,
            #     colkey=0
            # )

            # New 16x16 sprite rendering
            (u_ind, v_ind) = index
            pyxel.bltm(
                x=x,
                y=y,
                w=16,
                h=16,
                tm=0,
                u=u_ind * self.game.dim,
                v=v_ind * self.game.dim,
                colkey=0
            )
    
    def pre_draw_grid(self):
        pyxel.rect(0, 0, self.game.c*self.game.dim, self.game.r*self.game.dim, 0)
    
    def post_draw_grid(self):
        pyxel.text(0,0,f"Lives: {self.game.stage.get_lives()}",12)
        if self.game.currentGameState == GameState.READY:
            self.display_center_text("Press 0 to Start", 11)

        elif self.game.currentGameState != GameState.ONGOING:
            if self.game.currentGameState == GameState.WIN:
                self.display_center_text("VICTORY", 12)
                self.display_center_text("Press 2 to Next Stage", 11, 0, pyxel.FONT_HEIGHT * 2)

            elif self.game.currentGameState == GameState.LOSE:
                self.display_center_text("YOU DIED", 8)
            
            self.display_center_text("Press 1 to Restart Stage", 11, 0, pyxel.FONT_HEIGHT * 3)
            self.display_center_text("Press 0 to Start at Stage 1", 11, 0, pyxel.FONT_HEIGHT * 4)
            
            
    
    def display_center_text(self, s: str, col: int, x_offset: int = 0, y_offset: int = 0):
        pyxel.text((pyxel.width - (len(s) * pyxel.FONT_WIDTH)) / 2 + x_offset, (pyxel.height / 2) + y_offset, s, col)