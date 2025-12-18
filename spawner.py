# spawner.py
import random
from entities.enemies.registry import ENEMY_REGISTRY

class EnemySpawner:
    def __init__(self, pool, cfg_module, spawn_y=680, interval_min=1.2, interval_max=2.5, max_enemies=6):
        self.pool = pool                  # config.ENEMY_POOL
        self.cfg_module = cfg_module      # config module zelf
        self.spawn_y = spawn_y
        self.interval_min = interval_min
        self.interval_max = interval_max
        self.max_enemies = max_enemies

        self.timer = 0.0
        self.next_interval = random.uniform(interval_min, interval_max)

    def reset(self):
        self.timer = 0.0
        self.next_interval = random.uniform(self.interval_min, self.interval_max)

    def _pick_enemy_spec(self):
        weights = [e["weight"] for e in self.pool]
        spec = random.choices(self.pool, weights=weights, k=1)[0]
        return spec

    def update(self, dt, player, enemies, world_width=6000):
        if len(enemies) >= self.max_enemies:
            return

        self.timer += dt
        if self.timer < self.next_interval:
            return

        self.timer = 0.0
        self.next_interval = random.uniform(self.interval_min, self.interval_max)

        px = player.rect.centerx
        x = px + random.randint(-600, 600)
        x = max(50, min(world_width - 50, x))

        spec = self._pick_enemy_spec()

        enemy_cls = ENEMY_REGISTRY[spec["type"]]
        enemy_cfg = getattr(self.cfg_module, spec["cfg_key"])  # "ZOMBIE" -> config.ZOMBIE

        enemies.append(enemy_cls(x, self.spawn_y, enemy_cfg))