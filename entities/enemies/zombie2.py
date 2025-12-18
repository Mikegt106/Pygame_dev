from entities.enemies.zombie import Zombie
from entities.enemies.registry import register_enemy

class Zombie2(Zombie):
    pass

register_enemy("zombie2", Zombie2)