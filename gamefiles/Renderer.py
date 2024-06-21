from __future__ import annotations
from typing import TYPE_CHECKING, Any, get_args
from collections.abc import Callable

import pyxel

if TYPE_CHECKING:
    from gamefiles.GameField import GameField

from objects.Entity import Entity
from objects.Tank import Tank
from objects.Bullet import Bullet
from objects.Brick import Brick
from objects.Forest import Forest
from objects.Mirror import Mirror

from misc.util import Orientation, GameState

import resources.assetindex as assetindex

'''
Singleton for rendering
Renderer
    init()
        - called on GameField initialization
    draw_cell()
        - store all objects into a dictionary
            - x
            - y
            - index
                (u, v) on tilemap, disregards cell dimension (for easier indexing)
            - zIndex
                - z-order of object to allow for Forest cell to cover things, as well as other necessary ordering
                ORDER: (top-to-bottom is higher to lower priority)
                    - Bullet (3)
                    - Forest Cell (2)
                    - Tank (1)
                    - any other GameObject
    pre_draw_grid()
        - draws black background
        - resets the dictionary for every frame
    post_draw_grid()
        - lives counter
        - enemy counter
        - victory/lose text
        - game restart/next stage buttons text
        
        - draws all objects in the draw_cell() dictionary, sorted by zIndex
        - draws all custom renders
    
    display_center_text(s: str, col: int, x_offset: int = 0, y_offset: int = 0)
    render_custom(f: Callable[[], None], duration: int)
        - call a per-frame custom renderer function for a certain duration
'''

class Renderer:
    def __init__(self, game: GameField):
        self.game = game
        self._entities: dict[Entity, dict[str, Any]] = {}
        self._zOrder = list[dict[str, Any]]()
        self._customRenders = dict[Callable[[], None], dict[str, float]]()
    
    def init(self):
        pass

    def draw_cell(self, frame_count: int, i: int, j: int, x: int, y: int):
        if self.game.currentGameState == GameState.READY:
            return
        
        if (x, y) in self.game.stage.get_enemy_spawns():
            ...
            # (u_ind, v_ind) = 
            # pyxel.bltm(
            #     x=x,
            #     y=y,
            #     w=16,
            #     h=16,
            #     tm=0,
            #     u=u_ind * self.game.dim,
            #     v=v_ind * self.game.dim,
            #     colkey=0
            # )

        cell = self.game[i, j]
        for obj in cell.get_objects():

            obj_class = type(obj)
            index = assetindex.sprites[obj_class]
            z_index = 0
            

            if isinstance(obj, Entity):

                if isinstance(obj, Tank):
                    offset = 0
                    if obj.type == "Light":
                        offset = 8
                    elif obj.type == "Armored":
                        offset = 12
                    elif obj.team == "enemy":
                        offset = 4
                    index = index[offset + get_args(Orientation).index(obj.orientation)]
                    z_index = 1
                elif isinstance(obj, Bullet):
                    index = index[get_args(Orientation).index(obj.orientation)]
                    z_index = 3
                else:
                    index = index[0]

            elif isinstance(obj, Mirror):
                index = index[0 if obj.reflectOrientation == "northeast" else 1]
            elif isinstance(obj, Brick):
                index = index[0 if not obj.cracked else 1]
            else:
                if isinstance(obj, Forest):
                    z_index = 2
                index = index[0]

            self._zOrder.append({
                "x": x,
                "y": y,
                "index": index,
                "zIndex": z_index
            })
            
    
    def pre_draw_grid(self):
        pyxel.rect(0, 0, self.game.c*self.game.dim, self.game.r*self.game.dim, 0)
        self._zOrder = list[dict[str, Any]]()
    
    def post_draw_grid(self):
        pyxel.text(1,1,f"Lives: {self.game.stage.get_lives()}",12)

        enemy_count = f"Enemies Left: {self.game.stage.get_total_enemy_count()}"
        pyxel.text(pyxel.width-(len(enemy_count)*pyxel.FONT_WIDTH)-1,1,enemy_count,8)

        if self.game.currentGameState == GameState.READY:
            self.display_center_text("Press 0 to Start", 11)
            return

        elif self.game.currentGameState != GameState.ONGOING:
            if self.game.currentGameState == GameState.WIN:
                self.display_center_text("VICTORY", 12)
                self.display_center_text("Press 1 to Next Stage", 11, 0, pyxel.FONT_HEIGHT * 2)

            elif self.game.currentGameState == GameState.LOSE:
                self.display_center_text("HOME CELL WAS DESTROYED" if True in {h.is_destroyed() for h in self.game.stage.get_homes()} else "YOU DIED", 8)

            self.display_center_text("Press 0 to Start at Beginning", 11, 0, pyxel.FONT_HEIGHT * 3)
        
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
        self._zOrder.sort(key=lambda e: e["zIndex"])
        for data in self._zOrder:
            (u_ind, v_ind) = data["index"]
            pyxel.bltm(
                x=data["x"],
                y=data["y"],
                w=16,
                h=16,
                tm=0,
                u=u_ind * self.game.dim,
                v=v_ind * self.game.dim,
                colkey=0
            )
        
        # custom renders
        for f in list(self._customRenders):
            data = self._customRenders[f]
            data["frameCount"] += 1
            if data["frameCount"] > self.game.FPS * data["duration"]:
                del self._customRenders[f]
                continue
            f()
            
    def display_center_text(self, s: str, col: int, x_offset: int = 0, y_offset: int = 0):
        pyxel.text((pyxel.width - (len(s) * pyxel.FONT_WIDTH)) / 2 + x_offset, (pyxel.height / 2) + y_offset, s, col)
    def render_custom(self, f: Callable[[], None], duration: int):
        self._customRenders[f] = {
            "duration": duration,
            "frameCount": 0
        }