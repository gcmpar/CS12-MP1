from __future__ import annotations
from typing import TYPE_CHECKING, Any, get_args
from collections.abc import Callable

import pyxel

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from objects.GameObject import GameObject

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
                    - Explode effect (5)
                    - Bullet (4)
                    - Fire Effect (3)
                    - Forest Cell (2)
                    - Tank (1)
                    - any other GameObject (0)
                    - Tank Spawning (-1)
                    - Spawn, EnemySpawn (-2)
                    - POWERUP: Mirage effect (-3)

    pre_draw_grid()
        - draws black background
        - resets the dictionary for every frame
    post_draw_grid()
        - lives counter
        - enemy counter
        - stage number
        - victory/lose text
        - game restart/next stage buttons text
        
        - draws all objects in the draw_cell() dictionary, sorted by zIndex
        - draws all custom renders
    
    display_center_text(s: str, col: int, x_offset: int = 0, y_offset: int = 0)
    render_custom(f: Callable[[], None], duration: float)
        - call a per-frame custom renderer function for a certain duration
    stop_render_custom(f: Callable[[], None])
        
    render_z(x: int, y: int, index: tuple[int, int], zIndex: int)
        - insert into next z-order rendering
        - index is assetindex
        - zIndex is z-order
        - NOTE: x, y are WINDOW width/height, NOT cell index
        - NOTE: use self.game.x/self.game.y to convert cell coords
'''

class Renderer:
    def __init__(self, game: GameField):
        self.game = game
        self._entities: dict[Entity, dict[str, Any]] = {}
        self._zOrder = list[dict[str, Any]]()
        self._customRenders = dict[Callable[[], None], dict[str, Any]]()
        self._zOrderQueue = list[dict[str, Any]]()
    
    def init(self):
        def initialize(obj: GameObject):
            if self.game.get_game_state() == GameState.GENERATING:
                return
            if isinstance(obj, Bullet) or isinstance(obj, Tank):
                # bullet fire
                if isinstance(obj, Bullet):
                    def scope(o: GameObject):
                        duration = 0.1
                        f = 0
                        def fire_render():
                            if self.game.get_game_state() == GameState.GENERATING:
                                return
                            nonlocal f
                            f += 1
                            index = 0 if f <= self.game.FPS * duration/2 else 1

                            cell = o.get_cell()
                            x, y = cell.x, cell.y
                            self.render_z(x=self.game.x(x), y=self.game.y(y), index=assetindex.sprites["Explode"][index], z_index=3)
                        self.render_custom(fire_render, duration=duration)
                    scope(obj)

                # on destroy
                def scope2(o: GameObject):
                    def render():
                        if self.game.get_game_state() == GameState.GENERATING:
                            return
                        
                        cell = o.get_cell()
                        x, y = cell.x, cell.y
                        self.render_z(x=self.game.x(x), y=self.game.y(y), index=assetindex.sprites["Explode"][0], z_index=5)
                    
                    def on_explode():
                        if self.game.get_game_state() == GameState.GENERATING:
                            return
                        self.render_custom(render, duration=0.35)

                    o.onDestroy.add_listener(on_explode)
                scope2(obj)
                
        self.game.onObjectAdded.add_listener(initialize)


    def draw_cell(self, frame_count: int, i: int, j: int, x: int, y: int):
        if self.game.get_game_state() == GameState.READY:
            return
        
        if (j, i) in self.game.stage.get_enemy_spawns():
            self._zOrder.append({
                "x": x,
                "y": y,
                "index": assetindex.sprites["EnemySpawn"][0],
                "zIndex": -2,
            })
        if (j, i) == self.game.stage.get_spawn():
            self._zOrder.append({
                "x": x,
                "y": y,
                "index": assetindex.sprites["Spawn"][0],
                "zIndex": -2,
            })

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
                    has_mirage: bool = False
                    for mod in obj.modifiers:
                        if mod.type == "Mirage":
                            self._zOrder.append({
                                "x": x,
                                "y": y,
                                "index": assetindex.sprites["Mirage"][0],
                                "zIndex": -3,
                            })
                            has_mirage = True
                            break
                    if has_mirage:
                        continue
                elif isinstance(obj, Bullet):
                    index = index[get_args(Orientation).index(obj.orientation)]
                    z_index = 4
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
        if pyxel.btn(pyxel.KEY_CTRL):
            debug_text = "DEBUG"
            pyxel.text(1,pyxel.height-pyxel.FONT_HEIGHT-1,debug_text,8)

        current_state = self.game.get_game_state()
        if current_state == GameState.READY:
            self.display_center_text("Press 1 to Start", 11)
            self.display_center_text("Battle Tanks Bootleg TM", 2, 0, -pyxel.FONT_HEIGHT*2)
            return
        

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
        for data in self._zOrderQueue:
            self._zOrder.append(data)
        self._zOrderQueue = []
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
                self.stop_render_custom(f)
                continue
            f()

        lives_count = f"Lives: {self.game.stage.get_lives()}"
        pyxel.text(1,1,lives_count,12)

        enemy_count = f"Enemies Left: {self.game.stage.get_total_enemy_count()}"
        pyxel.text(pyxel.width-(len(enemy_count)*pyxel.FONT_WIDTH)-1,1,enemy_count,8)

        stage_number = f"Stage {str(self.game.currentStage)}"
        pyxel.text(pyxel.width-(len(stage_number)*pyxel.FONT_WIDTH)-1,pyxel.height-pyxel.FONT_HEIGHT-1,stage_number,7)

        if current_state == GameState.WIN or current_state == GameState.LOSE:
            if current_state == GameState.WIN:
                # Change this for more stages ig
                if self.game.currentStage >= 3:
                    self.display_center_text("GAME WON !!! :D", 10)
                    self.display_center_text("Press 2 to Repeat", 11, 0, pyxel.FONT_HEIGHT * 2)
                else:
                    self.display_center_text("VICTORY", 12)
                    self.display_center_text("Press 2 to Advance", 11, 0, pyxel.FONT_HEIGHT * 2)

            elif current_state == GameState.LOSE:
                self.display_center_text("HOME CELL WAS DESTROYED" if True in {h.is_destroyed() for h in self.game.stage.get_homes()} else "YOU DIED", 8)

            self.display_center_text("Press 1 to Restart", 11, 0, pyxel.FONT_HEIGHT * 3)
            
    def display_center_text(self, s: str, col: int, x_offset: int = 0, y_offset: int = 0):
        pyxel.text((pyxel.width - (len(s) * pyxel.FONT_WIDTH)) / 2 + x_offset, (pyxel.height / 2) + y_offset, s, col)
    
    def render_custom(self, f: Callable[[], None], duration: float, callback: Callable[[], None] | None = None):
        if f in self._customRenders.keys():
            return
        def c():
            pass
        self._customRenders[f] = {
            "duration": duration,
            "frameCount": 0,
            "callback": callback if callback is not None else c
        }
    def stop_render_custom(self, f: Callable[[], None]):
        if f not in self._customRenders.keys():
            return
        c = self._customRenders[f]["callback"]
        del self._customRenders[f]
        c()

    def render_z(self, x: int, y: int, index: tuple[int, int], z_index: int):
        self._zOrderQueue.append({
            "x": x,
            "y": y,
            "index": index,
            "zIndex": z_index
        })