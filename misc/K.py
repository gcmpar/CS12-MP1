from __future__ import annotations
from typing import TYPE_CHECKING

import pyxel

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from objects.GameObject import GameObject

from misc.util import Orientation, orientation_to_move_vector, orientation_to_ref_vector, flip_orientation
from objects.Mirror import Mirror
from objects.Entity import Entity
from objects.Brick import Brick
from objects.Home import Home
from objects.Karma import Karma

from resources.assetindex import ASSET_INDEX

def K(game: GameField, x: int, y: int, ori: Orientation):
    caught_mirrors: list[GameObject] = []
    count = 0
    def rec(x: int = x, y: int = y, ori: Orientation = ori):
        if not game.in_bounds(y, x):
            return
        nonlocal count
        count += 1
        
        cell = game[y, x]
        current_ori = ori
        for obj in cell.get_objects():
            if isinstance(obj, Mirror):
                if obj not in caught_mirrors:
                    caught_mirrors.append(obj)
                    ori = orientation_to_ref_vector(ori, obj.reflectOrientation)

            elif isinstance(obj, Karma):
                if obj not in caught_mirrors:
                    caught_mirrors.append(obj)
                ori = flip_orientation(ori)
            elif isinstance(obj, Entity) or isinstance(obj, Brick) or isinstance(obj, Home):
                obj.destroy()
            
        x_move, y_move = orientation_to_move_vector(ori)
        f = 0
        duration = 0.6
        current_count = count
        def render():
            nonlocal f
            f += 1
            if f <= game.FPS * (duration/2.25):
                i = 0
                i2 = 6
            elif f <= game.FPS * (duration/1.5):
                i = 2
                i2 = 7
            else:
                i = 4
                i2 = 8
            if ori == "north" or ori == "south":
                i += 1

            game.renderer.render_z(x=game.x(x) + (x_move/2 * game.dim), y=game.y(y) + (y_move/2 * game.dim), index=ASSET_INDEX["K"][i], z_index=69)

            if current_ori != ori or current_count == 1:
                game.renderer.render_z(x=game.x(x), y=game.y(y), index=ASSET_INDEX["K"][i2], z_index=69)
        game.renderer.render_custom(render, duration=duration)

        new_x = x + x_move
        new_y = y + y_move
        rec(new_x, new_y, ori)
    rec()
    pyxel.stop()
    pyxel.play(1, pyxel.sounds[3])
    pyxel.play(2, pyxel.sounds[4])
        
