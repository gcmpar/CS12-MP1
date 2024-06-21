from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gamefiles.GameField import GameField

from typing import TypeVar, ParamSpec, Generic
from collections.abc import Callable

P = ParamSpec("P")
R = TypeVar("R")

'''
Events implementation
NOTE: cleanup (destroy) is handled asynchronously

Signal(Generic[P, R])
    add_listener(f: Callable[P, R])
    remove_listener(f: Callable[P, R])

    fire(*args, **kwargs)
        - dispatcher

    remove_listeners()

    is_destroyed() -> bool
    destroy()

'''

class Signal(Generic[P, R]):
    _destroyed: bool
    _dq: bool
    def __init__(self, game: GameField):
        self.game = game
        self._listeners = list[Callable[P, R]]()
        self._destroyed = False
        self._dq = False

    def add_listener(self, f: Callable[P, R]):
        if self.is_destroyed():
            return
        if f in self._listeners:
            return
        self._listeners.append(f)
    def remove_listener(self, f: Callable[P, R]):
        if self.is_destroyed():
            return
        if f not in self._listeners:
            return
        self._listeners.remove(f)

    def fire(self, *args: P.args, **kwargs: P.kwargs):
        if self.is_destroyed():
            return
        for f in self._listeners:
            f(*args, **kwargs)
    
    def remove_listeners(self):
        self._listeners = []

    def is_destroyed(self) -> bool:
        return self._destroyed

    def destroy(self):
        if self.is_destroyed():
            return
        if self._dq:
            return
        self._dq = True

        def f():
            self._destroyed = True
            self._listeners = []
        self.game.queue_signal_destroy(f)
