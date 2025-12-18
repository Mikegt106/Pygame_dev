# wave_system.py

class WaveSystem:
    def __init__(
        self,
        break_time: float = 4.0,
        fight_time: float = 18.0,
        interval_min_start: float = 1.6,
        interval_max_start: float = 2.8,
        max_enemies_start: int = 6,
    ):
        self.break_time = break_time
        self.fight_time = fight_time

        self.interval_min_start = interval_min_start
        self.interval_max_start = interval_max_start
        self.max_enemies_start = max_enemies_start

        self.wave = 0
        self.state = "BREAK"
        self.timer = 0.0

    def start(self):
        self.wave = 0
        self._start_break()

    def is_fight(self):
        return self.state == "FIGHT"

    def _start_fight(self):
        self.wave += 1
        self.state = "FIGHT"
        self.timer = self.fight_time

    def _start_break(self):
        self.state = "BREAK"
        self.timer = self.break_time

    def apply_to_spawner(self, spawner):
        # scaling per wave
        w = self.wave

        # spawn sneller
        spawner.interval_min = max(0.45, self.interval_min_start - 0.08 * (w - 1))
        spawner.interval_max = max(0.85, self.interval_max_start - 0.10 * (w - 1))

        # meer enemies
        spawner.max_enemies = self.max_enemies_start + (w - 1)

    def update(self, dt: float, spawner):
        self.timer -= dt

        if self.timer <= 0:
            if self.state == "BREAK":
                self._start_fight()
            else:
                self._start_break()

        # telkens updaten zodat spawner scaling volgt
        if self.wave > 0:
            self.apply_to_spawner(spawner)