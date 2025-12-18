# wave_system.py

class WaveSystem:
    def __init__(self, waves: dict, break_time: float = 4.0):
        self.waves = waves
        self.break_time = break_time

        self.wave = 0
        self.state = "BREAK"   # BREAK | FIGHT
        self.timer = 0.0

        self.spawned = 0
        self.spawn_limit = 0

        # toast
        self.toast_text = ""
        self.toast_timer = 0.0
        self.toast_duration = 1.6

    def start(self):
        self.wave = 0
        self._start_break()

    def is_fight(self):
        return self.state == "FIGHT"

    def can_spawn(self):
        return self.is_fight() and (self.spawned < self.spawn_limit)

    def on_spawned(self, n: int = 1):
        self.spawned += n

    def _start_fight(self):
        self.wave += 1
        if self.wave not in self.waves:
            self.wave = max(self.waves.keys())

        wcfg = self.waves[self.wave]
        self.spawned = 0
        self.spawn_limit = int(wcfg.get("total_spawns", wcfg.get("max_enemies", 4)))

        self.state = "FIGHT"

    def _start_break(self, cleared_wave: int | None = None):
        self.state = "BREAK"
        self.timer = self.break_time

        if cleared_wave is not None:
            self.toast_text = f"WAVE {cleared_wave} CLEARED!"
            self.toast_timer = self.toast_duration

    def apply_to_spawner(self, spawner):
        wcfg = self.waves[self.wave]
        spawner.set_pool(wcfg["pool"])
        spawner.set_interval(*wcfg["interval"])
        spawner.set_max_enemies(wcfg["max_enemies"])
        spawner.reset()  # ✅ timer herrollen met nieuwe intervals

    def update(self, dt: float, spawner, enemies: list):
        # toast timer
        if self.toast_timer > 0:
            self.toast_timer = max(0.0, self.toast_timer - dt)
            if self.toast_timer == 0:
                self.toast_text = ""

        if self.state == "BREAK":
            self.timer -= dt
            if self.timer <= 0 and len(enemies) == 0:
                self._start_fight()
                self.apply_to_spawner(spawner)
            return

        # FIGHT:
        # wave is “klaar” als quota gespawned én er zijn geen enemies meer
        if (self.spawned >= self.spawn_limit) and (len(enemies) == 0):
            self._start_break(cleared_wave=self.wave)

    def get_toast_alpha(self) -> int:
        if self.toast_timer <= 0:
            return 0
        half = self.toast_duration * 0.25
        if self.toast_timer > (self.toast_duration - half):
            t = 1.0 - (self.toast_timer - (self.toast_duration - half)) / half
        elif self.toast_timer < half:
            t = self.toast_timer / half
        else:
            t = 1.0
        return max(0, min(255, int(255 * t)))