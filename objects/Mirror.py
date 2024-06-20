from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from misc.util import ReflectOrientation

from objects.Item import Item

class Mirror(Item):
    def __init__(self, game: GameField, x: int, y: int, ref_ori: ReflectOrientation):
        super().__init__(game, x, y)
        self.reflectOrientation = ref_ori