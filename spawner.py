# spawner.py
import random


class EnemySpawner:
    def __init__(
        self,
        enemy_cls,
        enemy_cfg: dict,
        spawn_y: int,
        interval_min: float = 1.2,
        interval_max: float = 2.5,
        max_enemies: int = 6,
        min_dist_from_player: int = 250,
        spawn_ahead_min: int = 400,
        spawn_ahead_max: int = 900,
        spawn_behind_chance: float = 0.20,
    ):
        self.enemy_cls = enemy_cls
        self.enemy_cfg = enemy_cfg
        self.spawn_y = spawn_y

        self.interval_min = interval_min
        self.interval_max = interval_max
        self.max_enemies = max_enemies

        self.min_dist_from_player = min_dist_from_player
        self.spawn_ahead_min = spawn_ahead_min
        self.spawn_ahead_max = spawn_ahead_max
        self.spawn_behind_chance = spawn_behind_chance

        self.timer = 0.0
        self.next_spawn = random.uniform(self.interval_min, self.interval_max)

    def reset(self):
        self.timer = 0.0
        self.next_spawn = random.uniform(self.interval_min, self.interval_max)

    def _pick_spawn_x(self, player_x: float, world_width: int | None):
        # meestal voor de player, soms achter
        behind = random.random() < self.spawn_behind_chance
        if behind:
            dx = random.uniform(self.spawn_ahead_min, self.spawn_ahead_max)
            x = player_x - dx
        else:
            dx = random.uniform(self.spawn_ahead_min, self.spawn_ahead_max)
            x = player_x + dx

        # clamp in world
        if world_width is not None:
            x = max(0, min(world_width, x))

        return x

    def update(self, dt: float, player, enemies: list, world_width: int | None = None):
        # tel alleen levende enemies mee (dode mogen nog liggen/faden)
        alive = sum(1 for e in enemies if not getattr(e, "dead", False))
        if alive >= self.max_enemies:
            return

        self.timer += dt
        if self.timer < self.next_spawn:
            return

        self.timer = 0.0
        self.next_spawn = random.uniform(self.interval_min, self.interval_max)

        px = player.rect.centerx
        x = self._pick_spawn_x(px, world_width)

        # niet te dicht bij player
        if abs(x - px) < self.min_dist_from_player:
            x = px + (self.min_dist_from_player if x >= px else -self.min_dist_from_player)
            if world_width is not None:
                x = max(0, min(world_width, x))

        enemies.append(self.enemy_cls(int(x), self.spawn_y, self.enemy_cfg))