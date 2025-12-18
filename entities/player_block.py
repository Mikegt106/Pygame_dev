# entities/player_block.py
import math
import random
import pygame
from assets import load_image


class BlockResult:
    NONE = 0
    SUCCESS = 1
    FAIL = 2


class BlockSystem:
    def __init__(
        self,
        shield_path="assets/HealthbarUI/Blockshield.png",
        shield_scale=0.1,
        block_chance=0.60,
        fail_stun=0.40,
        cooldown=0.5,
        pushback_force=350.0,   # ✅ TUNE: hoe hard je terugduwt bij success
    ):
        self.blocking = False

        self.block_chance = block_chance
        self.fail_stun = fail_stun

        self.cooldown_duration = float(cooldown)
        self.cooldown_timer = 0.0

        self.pushback_force = float(pushback_force)

        self.shield_img = load_image(shield_path, alpha=True, scale=shield_scale)

        self.shield_timer = 0.0
        self.shield_duration = 0.18

        self.fail_fx_timer = 0.0
        self.fail_fx_duration = 0.22

        self.hit_pop_timer = 0.0
        self.hit_pop_duration = 0.10

        self._t = 0.0

    def update(self, dt: float, protecting_key: bool):
        self._t += dt

        if self.cooldown_timer > 0:
            self.cooldown_timer = max(0.0, self.cooldown_timer - dt)

        # alleen blocken als geen cooldown
        self.blocking = protecting_key and (self.cooldown_timer <= 0)

        # timers
        if self.shield_timer > 0:
            self.shield_timer = max(0.0, self.shield_timer - dt)
        if self.fail_fx_timer > 0:
            self.fail_fx_timer = max(0.0, self.fail_fx_timer - dt)
        if self.hit_pop_timer > 0:
            self.hit_pop_timer = max(0.0, self.hit_pop_timer - dt)

    def try_block(self):
        """
        Call ONLY when enemy actually hits.
        Returns (BlockResult, pushback_force)
        """
        if not self.blocking:
            return BlockResult.NONE, 0.0

        if random.random() <= self.block_chance:
            # ✅ SUCCESS
            self.shield_timer = self.shield_duration
            self.hit_pop_timer = self.hit_pop_duration
            return BlockResult.SUCCESS, self.pushback_force

        # ❌ FAIL
        self.fail_fx_timer = self.fail_fx_duration
        self.cooldown_timer = self.cooldown_duration
        return BlockResult.FAIL, 0.0

    def get_fail_stun(self) -> float:
        return self.fail_stun

    def draw_shield(self, screen: pygame.Surface, player_rect: pygame.Rect, facing_right: bool):
        # alleen tekenen wanneer hit gebeurd is (success of fail)
        if self.shield_timer <= 0 and self.fail_fx_timer <= 0:
            return

        s = self.shield_img.copy()
        pulse = (math.sin(self._t * 14.0) + 1.0) * 0.5
        add = int(90 * pulse)

        if self.fail_fx_timer > 0:
            # red pulse
            s.fill((add + 60, 0, 0), special_flags=pygame.BLEND_RGB_ADD)
        else:
            # green/white pulse
            s.fill((0, add + 30, 0), special_flags=pygame.BLEND_RGB_ADD)
            s.fill((add, add, add), special_flags=pygame.BLEND_RGB_ADD)

        direction = 1 if facing_right else -1
        shield_x = player_rect.centerx + direction * 35
        shield_y = player_rect.centery - 20

        sr = s.get_rect(center=(shield_x, shield_y))
        screen.blit(s, sr)