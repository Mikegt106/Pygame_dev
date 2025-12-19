from entities.enemies.skeleton import Skeleton
from entities.enemies.registry import register_enemy

class Skeleton2(Skeleton):
    pass

register_enemy("skeleton2", Skeleton2)