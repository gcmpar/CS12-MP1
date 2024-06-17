from __future__ import annotations
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from objects.GameObject import GameObject

from objects.Entity import Entity

class PhysicsManager:
    def __init__(self, game: GameField):
        self.game = game
        self._entities: dict[Entity, dict[str, Any]] = {}
    
    def update(self, frame_count: int):
        
        # check collision moving
        for entity in list(self._entities):
            if entity.is_destroyed():
                del self._entities[entity]
                continue

            if entity.speed == 0:
                continue

            data = self._entities[entity]

            if frame_count < (data["last_move_frame"] + (self.game.FPS / entity.speed)):
                continue
            data["last_move_frame"] = frame_count
            
            cell = entity.get_cell()
            ori = entity.orientation
            x_move = 1 if ori == "east" else -1 if ori == "west" else 0
            y_move = 1 if ori == "south" else -1 if ori == "north" else 0

            new_x = cell.x + x_move
            new_y = cell.y + y_move

            if not self.game.in_bounds(new_y, new_x):
                entity.main_out_of_bounds()
                continue

            new_cell = self.game[new_y, new_x]

            if self.can_move_to(entity, new_x, new_y):
                entity.move_to(new_x, new_y)
            else:
                for other in new_cell.get_objects():
                    
                    if entity.is_destroyed():
                        break
                    if entity == other:
                        continue
                    if other.is_destroyed():
                        continue

                    if entity.can_collide(other) and other.can_collide(entity):

                        entity.main_collided_with(other)
                        other.main_collided_with(entity)

        # check collision same cell
        caught: dict[GameObject, list[GameObject]] = {}
        for r in range(self.game.r):
            for c in range(self.game.c):
                cell = self.game[r, c]
                
                for obj in cell.get_objects():

                    if isinstance(obj, Entity):
                        if obj not in self._entities.keys():
                            self._entities[obj] = {
                                "last_move_frame": frame_count
                            }

                    for other in cell.get_objects():

                        if obj.is_destroyed():
                            break
                        if obj == other:
                            continue
                        if other.is_destroyed():
                            continue

                        if obj not in caught.keys():
                            caught[obj] = []
                        if other not in caught.keys():
                            caught[other] = []
                            
                        if obj in caught[other] or other in caught[obj]:
                            continue

                        if obj.can_collide(other) and other.can_collide(obj):

                            obj.main_collided_with(other)
                            other.main_collided_with(obj)

                            keys = caught.keys()
                            if obj not in keys:
                                caught[obj] = []
                            if other not in keys:
                                caught[other] = []
                        
                        obj.main_touched(other)
                        other.main_touched(obj)

                        caught[obj].append(other)
                        caught[other].append(obj)

    def can_move_to(self, obj: GameObject, x: int, y: int) -> bool:
        target_cell = self.game[y, x]

        for other in target_cell.get_objects():
            if other == obj:
                continue
            if obj.can_collide(other) and other.can_collide(obj):
                return False
            
        return True