from objects.GameObject import GameObject
from objects.Item import Item

class Forest(Item):
    def can_collide(self, other: GameObject):
        return False
    def can_touch(self, other: GameObject):
        return False