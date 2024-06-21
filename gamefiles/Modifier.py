from __future__ import annotations
from typing import TYPE_CHECKING, Any
from collections.abc import Callable

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from objects.GameObject import GameObject

'''
Manipulator of the whole game
NOTE: if modifier needs to remove itself, please call object.remove_modifier() instead of modifier.destroy() !!
NOTE: modifier function must access tank with self.owner !!

Modifier
    game: GameField
    owner: GameObject
        - can be transferred!!
    priority: int
        - higher = run last
    
    data: dict[str, Any]
        - where modifier's functions can store its any data it needs throughout its lifetime
        - instead of using nonlocal/global variables in functions defined outside Modifier's creation,
            this can instead be used
        - this allows for modifier copying
    
    copy(copy_data: bool = False) -> Modifier
        - returns a copy of the modifier
    
    init()
        - called whenever added to an object

    update(frame_count: int)
        - called everytime object is updated

    destroy()
        - called whenever removed from object

    can_collide() -> bool | None
        - if returns bool, overrides object.can_collide()
    can_touch() -> bool | None
        - if returns bool, overrides object.can_touch()
'''

class Modifier:
    init: Callable[[Modifier], None]
    update: Callable[[Modifier, int], None]
    destroy: Callable[[Modifier], None]
    can_collide: Callable[[Modifier, GameObject], bool | None]
    can_touch: Callable[[Modifier, GameObject], bool | None]
    def __init__(self, game: GameField, owner: GameObject, priority: int | None = None,
                 init: Callable[[Modifier], None] | None = None,
                 update: Callable[[Modifier, int], None] | None = None,
                 destroy: Callable[[Modifier], None] | None = None,
                 can_collide: Callable[[Modifier, GameObject], bool | None] | None = None,
                 can_touch: Callable[[Modifier, GameObject], bool | None] | None = None,
                 data: dict[str, Any] | None = None):
        
        self.game = game
        self.owner = owner
        self.priority = priority if priority is not None else 0
        self.data = data if data is not None else dict[str, Any]()

        self.init = init if init is not None else lambda _: None
        self.update = update if update is not None else lambda _, f: None
        self.destroy = destroy if destroy is not None else lambda _: None
        self.can_collide = can_collide if can_collide is not None else lambda _, o: None
        self.can_touch = can_touch if can_touch is not None else lambda _, o: None
    
    def copy(self, copy_data: bool = False):
        return Modifier(
            game=self.game,
            owner=self.owner,
            priority=self.priority,
            init=self.init,
            update=self.update,
            destroy=self.destroy,
            can_collide=self.can_collide,
            can_touch=self.can_touch,
            data=self.data if copy_data else None
        )



        
