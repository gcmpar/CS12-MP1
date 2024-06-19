from typing import TypeVar, ParamSpec, Callable, Generic

P = ParamSpec("P")
R = TypeVar("R")

class Signal(Generic[P, R]):
    _destroyed: bool
    def __init__(self):
        self._listeners = list[Callable[P, R]]()
        self._destroyed = False

    def add_listener(self, f: Callable[P, R]):
        if self._destroyed:
            return
        if f in self._listeners:
            return
        self._listeners.append(f)
    def remove_listener(self, f: Callable[P, R]):
        if self._destroyed:
            return
        if f not in self._listeners:
            return
        self._listeners.remove(f)

    def fire(self, *args: P.args, **kwargs: P.kwargs):
        if self._destroyed:
            return
        for f in self._listeners:
            f(*args, **kwargs)
    
    def destroy(self):
        if self._destroyed:
            return
        self._listeners = []
