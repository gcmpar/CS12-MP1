'''
Stats value holder
For interaction with Modifier and powerups

Stat:
    base: float
        - base stat, not modified
    current: float
        - current stat, modified by Modifiers

'''
class Stat:
    def __init__(self, base: float, current: float | None = None):
        self.base = base
        self.current = current if current is not None else base