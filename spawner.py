import random
from enemies import Zombie


class EnemySpawner:
    def __init__(
        self,
        enemy_cfg,
        spawn_y,
        interval_min=1.5,
        interval_max=3.0,
        max_enemies=6,
    ):
        self.enemy_cfg = enemy_cfg
        self.spawn_y = spawn_y
        self.interval_min = interval_min
        self.interval_max = interval_max
        self.max_enemies = max_enemies

        self.timer = 0.0
        self._reset_timer()

    def _reset_timer(self):
        self.timer = random.uniform(self.interval_min, self.interval_max)

    def reset(self):
        self._reset_timer()

    def update(self, dt, player, zombies, world_width=6000):
        if len(zombies) >= self.max_enemies:
            return

        self.timer -= dt
        if self.timer > 0:
            return

        # spawn left or right of player
        side = random.choice([-1, 1])
        dist = random.randint(350, 900)
        x = player.rect.centerx + side * dist
        x = max(0, min(world_width, x))

        zombies.append(Zombie(x, self.spawn_y, self.enemy_cfg))
        self._reset_timer()