from __future__ import annotations
from typing import TYPE_CHECKING
from collections.abc import Callable

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from objects.GameObject import GameObject

'''
Manipulator of the whole game
NOTE: if modifier needs to remove itself, please call object.remove_modifier() instead of modifier.destroy() !!

Modifier
    game: GameField
    owner: GameObject

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
    init: Callable[[], None]
    update: Callable[[int], None]
    destroy: Callable[[], None]
    can_collide: Callable[[GameObject], bool | None]
    can_touch: Callable[[GameObject], bool | None] | None = None
    def __init__(self, game: GameField, owner: GameObject,
                 init: Callable[[], None] | None = None,
                 update: Callable[[int], None] | None = None,
                 destroy: Callable[[], None] | None = None,
                 can_collide: Callable[[GameObject], bool | None] | None = None,
                 can_touch: Callable[[GameObject], bool | None] | None = None,
                 ):
        
        self.game = game
        self.owner = owner

        self.init = init if init is not None else lambda: None
        self.update = update if update is not None else lambda f: None
        self.destroy = destroy if destroy is not None else lambda: None
        self.can_collide = can_collide if can_collide is not None else lambda o: None
        self.can_touch = can_touch if can_touch is not None else lambda o: None



        
