from __future__ import annotations
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from objects.GameObject import GameObject

from objects.Entity import Entity
from gamefiles.Cell import Cell

'''
Singleton for managing physics and Entity movement
Entity speed/movement is one cell every certain number of frames
Negative speed values is same as 0 (since Orientation determines vector direction anyway)
can_collide(), collided_with() and touched() are called on both for each other

init()
    - called on GameField initialization
update()
    - called every game loop
    - ORDER:
        - SAME-CELL COLLISION
            - call collided_with(), touched() on objects in same cell
                (this is for if there's somehow two GameObjects that were able to move into each other even if collidable)
        
        - MOVEMENT COLLISION
            - store entities that need to move (+ trigger OOB)
            - store entities that CAN move, and move them (+ trigger collision if can't)
            - trigger touched after all




'''

class PhysicsManager:
    def __init__(self, game: GameField):
        self.game = game
        self._entities: dict[Entity, dict[str, Any]] = {}
    
    def init(self):
        def reset():
            self._entities = {}
        self.game.stage.onStageGenerated.add_listener(reset)

    def update(self, frame_count: int):
        
        # same-cell collision
        collision_pairs: list[set[GameObject]] = []
        for r in range(self.game.r):
            for c in range(self.game.c):
                cell = self.game[r, c]
                
                for obj in cell.get_objects():

                    if isinstance(obj, Entity):
                        if obj not in self._entities.keys():
                            self._entities[obj] = {
                                "lastMoveFrame": -6969
                            }
                            
                    for other in cell.get_objects():
                        if other == obj:
                            continue
                        pair = {obj, other}
                        if pair in collision_pairs:
                            continue
                        collision_pairs.append(pair)

                        if obj.main_can_collide(other) and other.main_can_collide(obj):
                            obj.main_collided_with(other)
                            other.main_collided_with(obj)
                        if obj.main_can_touch(other) and other.main_can_touch(obj):
                            obj.main_touched(other)
                            other.main_touched(obj)
        
        # movement collision
        target_cell_map: dict[Entity, Cell] = {}

        # store entities that are supposed to move (+ trigger OOB)
        for entity in list(self._entities):
            if entity.is_destroyed():
                del self._entities[entity]
                continue

            cell = entity.get_cell()
            data = self._entities[entity]

            # speed guard
            if entity.speed == 0:
                continue
            if frame_count < (data["lastMoveFrame"] + (self.game.FPS / entity.speed)):
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
            
            new_cell = self.game[new_y, new_x]
            target_cell_map[entity] = new_cell
        
        # check collision for each
        # move if none
        collision_pairs: list[set[GameObject]] = []
        moved_entities: dict[Entity, Cell] = {}
        moved_adjacent: dict[Entity, list[Entity]] = {}
        for entity, target_cell in target_cell_map.items():
            can_move: bool = True
            current_cell = entity.get_cell()
            adjacent_entities: list[Entity] = []
            for other in target_cell.get_objects():
                if entity.main_can_collide(other) and other.main_can_collide(entity):
                    pair = {entity, other}
                    if pair not in collision_pairs:
                        collision_pairs.append(pair)
                        entity.main_collided_with(other)
                        other.main_collided_with(entity)
                    can_move = False

                # (**special) CHECK FOR ADJACENCY
                if isinstance(other, Entity) and other in target_cell_map.keys():
                    if target_cell_map[other] == current_cell: # if moving towards each other
                        adjacent_entities.append(other)
            
            if can_move:
                entity.move_to(target_cell.x, target_cell.y)
                self._entities[entity]["lastMoveFrame"] = frame_count
                moved_entities[entity] = target_cell
                moved_adjacent[entity] = adjacent_entities

        # (**special) TRIGGER TOUCHED
        touched_pairs: list[set[GameObject]] = []
        for entity, adjacent_entities in moved_adjacent.items():
            for other in adjacent_entities:
                if entity.main_can_touch(other) and other.main_can_touch(entity):
                    pair: set[GameObject] = {entity, other}
                    if pair not in touched_pairs:
                        touched_pairs.append(pair)
                        entity.main_touched(other)
                        other.main_touched(entity)


        # trigger touched
        for entity, target_cell in moved_entities.items():
            for other in target_cell.get_objects():
                if other == entity:
                    continue
                if entity.main_can_touch(other) and other.main_can_touch(entity):
                    pair = {entity, other}
                    if pair not in touched_pairs:
                        touched_pairs.append(pair)
                        entity.main_touched(other)
                        other.main_touched(entity)
                    

        




        
        