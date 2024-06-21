from __future__ import annotations
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from objects.GameObject import GameObject

from objects.Entity import Entity

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
            - for entities that need to move to a target cell at this exact frame
            - call collided_with() on (entity, other) where other is a collidable object on the target cell

        - MOVEMENT TOUCHED
            - trigger touched() on all entities that moved




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
                                "lastMoveFrame": -1
                            }
                            
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
                        if obj.can_touch(other) and other.can_touch(obj):
                            obj.main_touched(other)
                            other.main_touched(obj)
        
        # movement collision
        moved_entities: list[Entity] = []
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
            
            # check collision
            new_cell = self.game[new_y, new_x]
            can_move_to: bool = True
            for other in new_cell.get_objects():
                if other == entity:
                    continue

                if entity.can_collide(other) and other.can_collide(entity):
                    entity.main_collided_with(other)
                    other.main_collided_with(entity)
                    can_move_to = False
            
            if can_move_to:
                entity.move_to(new_x, new_y)
                moved_entities.append(entity)
                data["lastMoveFrame"] = frame_count
        
        # movement touched
        for obj in moved_entities:
            cell = obj.get_cell()
            for other in cell.get_objects():
                if other == obj:
                    continue

                if obj.can_touch(other) and other.can_touch(obj):
                    obj.main_touched(other)
                    other.main_touched(obj)

        
        