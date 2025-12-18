# spawner.py
import random
import pygame

from entities.enemies.registry import get_enemy_class


class EnemySpawner:
    """
    pool kan:
    - lijst van dicts: {"type": "zombie", "cfg_key": "ZOMBIE", "weight": 70}
    - lijst van tuples: ("zombie", "ZOMBIE", 70)
    """

    def __init__(
        self,
        pool,
        cfg_module,
        spawn_y: int,
        interval_min: float = 1.2,
        interval_max: float = 2.5,
        max_enemies: int = 6,
        spawn_pad: int = 700,
    ):
        self.pool = pool
        self.cfg = cfg_module
        self.spawn_y = spawn_y

        self.interval_min = interval_min
        self.interval_max = interval_max
        self.max_enemies = max_enemies
        self.spawn_pad = spawn_pad

        self.timer = 0.0
        self._reset_timer()

    def reset(self):
        self.timer = 0.0
        self._reset_timer()

    def _reset_timer(self):
        self.timer = random.uniform(self.interval_min, self.interval_max)

    def _normalize_spec(self, item):
        # dict-format
        if isinstance(item, dict):
            etype = item.get("type")
            cfg_key = item.get("cfg_key")
            weight = item.get("weight", 1)
            return etype, cfg_key, float(weight)

        # tuple/list-format: ("zombie","ZOMBIE",70)
        if isinstance(item, (tuple, list)) and len(item) >= 2:
            etype = item[0]
            cfg_key = item[1]
            weight = item[2] if len(item) >= 3 else 1
            return etype, cfg_key, float(weight)

        raise TypeError(f"Invalid enemy spec in pool: {item!r}")

    def _pick_enemy_spec(self):
        specs = [self._normalize_spec(x) for x in self.pool]
        weights = [w for (_, _, w) in specs]
        etype, cfg_key, _ = random.choices(specs, weights=weights, k=1)[0]
        return etype, cfg_key

    def spawn_one(self, player_x: float, world_width: int):
        etype, cfg_key = self._pick_enemy_spec()

        EnemyClass = get_enemy_class(etype)
        cfg_dict = getattr(self.cfg, cfg_key)

        # spawn links of rechts buiten beeld
        side = random.choice([-1, 1])
        x = player_x + side * self.spawn_pad

        # clamp binnen world
        x = max(80, min(world_width - 80, x))

        return EnemyClass(x, self.spawn_y, cfg_dict)

    def update(self, dt: float, player, enemies: list, world_width: int):
        if len(enemies) >= self.max_enemies:
            return

        self.timer -= dt
        if self.timer <= 0:
            enemies.append(self.spawn_one(player.rect.centerx, world_width))
            self._reset_timer()