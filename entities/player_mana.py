# entities/player_mana.py
class ManaSystem:
    def __init__(self, max_mana: float, drain_run=6.0, regen=2.0):
        self.max_mana = float(max_mana)
        self.mana = float(self.max_mana)

        self.drain_run = float(drain_run)
        self.regen = float(regen)

        self.exhausted = False  # lock sprint until full
        self.draining = False
        self.regening = False

    def update(self, dt: float, sprinting: bool, moving: bool):
        self.draining = False
        self.regening = False

        if self.mana <= 0:
            self.mana = 0.0
            self.exhausted = True

        if self.exhausted and self.mana >= self.max_mana:
            self.mana = self.max_mana
            self.exhausted = False

        if sprinting and moving and (not self.exhausted):
            self.draining = True
            self.mana -= self.drain_run * dt
            if self.mana <= 0:
                self.mana = 0.0
                self.exhausted = True
        else:
            if self.mana < self.max_mana:
                self.regening = True
                self.mana += self.regen * dt
                if self.mana > self.max_mana:
                    self.mana = self.max_mana