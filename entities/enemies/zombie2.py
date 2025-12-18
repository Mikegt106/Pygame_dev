from entities.enemies.registry import register_enemy
from entities.enemies.zombie import Zombie 

class Zombie2(Zombie):
    pass

register_enemy("zombie2", Zombie2)