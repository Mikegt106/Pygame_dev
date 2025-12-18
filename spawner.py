# spawner.py
import random
from entities.enemies.registry import get_enemy_class


class EnemySpawner:
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

        self.interval_min = float(interval_min)
        self.interval_max = float(interval_max)
        self.max_enemies = int(max_enemies)
        self.spawn_pad = int(spawn_pad)

        self.timer = 0.0
        self._reset_timer()

    def reset(self):
        self.timer = 0.0
        self._reset_timer()

    def _reset_timer(self):
        # safety: als min==max is uniform ook ok
        self.timer = random.uniform(self.interval_min, self.interval_max)

    def _normalize_spec(self, item):
        # dict-format
        if isinstance(item, dict):
            etype = item.get("type")
            cfg_key = item.get("cfg_key")
            weight = item.get("weight", 1)

            if not etype or not cfg_key:
                raise ValueError(f"Enemy spec missing 'type' or 'cfg_key': {item!r}")

            return etype, cfg_key, float(weight)

        # tuple/list-format: ("zombie","ZOMBIE",70)
        if isinstance(item, (tuple, list)) and len(item) >= 2:
            etype = item[0]
            cfg_key = item[1]
            weight = item[2] if len(item) >= 3 else 1
            return etype, cfg_key, float(weight)

        raise TypeError(f"Invalid enemy spec in pool: {item!r}")

    def set_pool(self, pool):
        self.pool = pool
        self._reset_timer()  # ✅ meteen effect

    def set_interval(self, interval_min, interval_max):
        self.interval_min = float(interval_min)
        self.interval_max = float(interval_max)
        self._reset_timer()  # ✅ meteen effect

    def set_max_enemies(self, n):
        self.max_enemies = int(n)

    def _pick_enemy_spec(self):
        if not self.pool:
            raise ValueError("EnemySpawner.pool is empty")

        specs = [self._normalize_spec(x) for x in self.pool]
        weights = [w for (_, _, w) in specs]

        etype, cfg_key, _ = random.choices(specs, weights=weights, k=1)[0]
        return etype, cfg_key

    def spawn_one(self, player_x: float, world_width: int):
        etype, cfg_key = self._pick_enemy_spec()

        EnemyClass = get_enemy_class(etype)
        cfg_dict = getattr(self.cfg, cfg_key)

        side = random.choice([-1, 1])
        x = player_x + side * self.spawn_pad
        x = max(80, min(world_width - 80, x))

        return EnemyClass(x, self.spawn_y, cfg_dict)

    def update(self, dt: float, player, enemies: list, world_width: int):
        if len(enemies) >= self.max_enemies:
            return

        self.timer -= dt
        if self.timer <= 0:
            enemies.append(self.spawn_one(player.rect.centerx, world_width))
            self._reset_timer()