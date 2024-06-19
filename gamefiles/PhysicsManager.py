from __future__ import annotations
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from gamefiles.Cell import Cell
    from objects.GameObject import GameObject

from objects.Entity import Entity

class PhysicsManager:
    def __init__(self, game: GameField):
        self.game = game
        self._entities: dict[Entity, dict[str, Any]] = {}
    
    def update(self, frame_count: int):
        
        collision_pairs: list[set[GameObject]] = []
        for r in range(self.game.r):
            for c in range(self.game.c):
                cell = self.game[r, c]
                
                for obj in cell.get_objects():

                    if isinstance(obj, Entity):
                        if obj not in self._entities.keys():
                            self._entities[obj] = {
                                "last_move_frame": -1
                            }

                    # check overlaps first
                    for other in cell.get_objects():
                        if other == obj:
                            continue
                        pair = {obj, other}
                        if pair in collision_pairs:
                            continue
                        collision_pairs.append(pair)

                        if obj.can_collide(other) and other.can_collide(obj):
                            obj.main_collided_with(other)
                            other.main_collided_with(obj)
                        
                        obj.main_touched(other)
                        other.main_touched(obj)


        # reset
        collision_pairs: list[set[GameObject]] = []
        
        # store entities that need to move at this frame
        # this is so entities don't trigger collision in-between if they "move out of the way" anyway in a later iteration
        moving_entities: dict[Entity, Cell] = {}
        target_cell_map: dict[Cell, list[Entity]] = {}
        for entity in list(self._entities):
            if entity.is_destroyed():
                del self._entities[entity]
                continue
            
            cell = entity.get_cell()
            data = self._entities[entity]

            # speed guard
            if entity.speed == 0:
                continue
            if frame_count < (data["last_move_frame"] + (self.game.FPS / entity.speed)):
                continue
            
            ori = entity.orientation
            x_move = 1 if ori == "east" else -1 if ori == "west" else 0
            y_move = 1 if ori == "south" else -1 if ori == "north" else 0

            new_x = cell.x + x_move
            new_y = cell.y + y_move

            # OOB guard
            if not self.game.in_bounds(new_y, new_x):
                entity.main_out_of_bounds()
                continue
            
            # store the target cell (cell where entity is supposed to move to at this frame)
            new_cell = self.game[new_y, new_x]
            moving_entities[entity] = new_cell

            if new_cell not in target_cell_map.keys():
                target_cell_map[new_cell] = []
            target_cell_map[new_cell].append(entity)

        
        # check collision on target cell
        movers = moving_entities.keys()
        valid_movers: list[Entity] = []
        for entity, target_cell in moving_entities.items():

            can_move_to: bool = True

            for other in target_cell.get_objects():
                if not (entity.can_collide(other) and other.can_collide(entity)):
                    continue

                if isinstance(other, Entity) and other in movers:
                    # if not moving towards each other then dont trigger collision
                    other_target = moving_entities[other]
                    if other_target != entity.get_cell() or target_cell != other.get_cell():
                        continue
                    
                can_move_to = False

                pair = {entity, other}
                if pair in collision_pairs:
                    continue
                collision_pairs.append(pair)
                
            if can_move_to:
                valid_movers.append(entity)
        
        # check collision on entities with same target cell
        for cell, entities in target_cell_map.items():
            for entity in entities:
                for other in entities:
                    
                    if other == entity:
                        continue
                    if not (entity.can_collide(other) and other.can_collide(entity)):
                        continue

                    target1 = moving_entities[entity]
                    target2 = moving_entities[other]
                    if target1 != target2:
                        continue

                    pair: set[GameObject] = {entity, other}
                    if pair in collision_pairs:
                        continue
                    collision_pairs.append(pair)
        
        # trigger collision
        for pair in collision_pairs:
            (obj, other) = tuple(pair)
            obj.main_collided_with(other)
            other.main_collided_with(obj)

        # move
        for entity in valid_movers:
            target_cell = moving_entities[entity]
            entity.move_to(target_cell.x, target_cell.y)
            self._entities[entity]["last_move_frame"] = frame_count