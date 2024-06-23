from __future__ import annotations
from typing import TYPE_CHECKING
from collections.abc import Callable

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from misc.util import ReflectOrientation
    from objects.GameObject import GameObject

from objects.Item import Item

class Mirror(Item):
    def __init__(self, game: GameField, x: int, y: int,
                 ref_ori: ReflectOrientation,

                 pre_added: Callable[[GameObject], bool] | None = None,
                 ):
        self.reflectOrientation = ref_ori
        super().__init__(game=game, x=x, y=y, pre_added=pre_added)