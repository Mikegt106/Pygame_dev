import pygame
import math
from assets import load_image


class StatBarUI:
    def __init__(self, pos=(60, 20), scale=1.8):
        self.pos = pygame.Vector2(pos)
        self.scale = scale

        # load + scale once (via cached loader)
        self.panel    = load_image("assets/HealthbarUI/HealthBarPanel_160x41.png", alpha=True, scale=scale)
        self.circle   = load_image("assets/HealthbarUI/BlackBigCircleBoxWithBorder_27x27.png", alpha=True, scale=scale)
        self.valuebar = load_image("assets/HealthbarUI/ValueBar_128x16.png", alpha=True, scale=scale)
        self.red      = load_image("assets/HealthbarUI/ValueRed_120x8.png", alpha=True, scale=scale)
        self.blue     = load_image("assets/HealthbarUI/ValueBlue_120x8.png", alpha=True, scale=scale)
        self.knot     = load_image("assets/HealthbarUI/CornerKnot_14x14.png", alpha=True, scale=scale)
        self.heart    = load_image("assets/HealthbarUI/Heart.png", alpha=True, scale=scale * 1.2)

        # mana container = dezelfde valuebar maar dunner in HEIGHT (breedte blijft identiek)
        vb_w = self.valuebar.get_width()
        vb_h = self.valuebar.get_height()
        self.mana_valuebar = pygame.transform.scale(self.valuebar, (vb_w, int(vb_h * 0.5)))

        # values
        self.max_hp = 200
        self.hp = 200
        self.max_mana = 50
        self.mana = 50

        # ---- flags from player ----
        self.mana_draining = False
        self.mana_regening = False
        self.mana_exhausted = False
        self._prev_exhausted = False

        # --- TUNE ---
        self.valuebar_offset = pygame.Vector2(30, 9) * scale

        # finetune offsets
        self.panel_offset    = pygame.Vector2(0, 0) * scale
        self.circle_nudge    = pygame.Vector2(-10, -4) * scale

        self.hp_bar_nudge    = pygame.Vector2(-13, -1.2) * scale
        self.mana_bar_nudge  = pygame.Vector2(-15, -1.6) * scale

        self.hp_fill_nudge   = pygame.Vector2(0, 0) * scale
        self.mana_fill_nudge = pygame.Vector2(0, -2) * scale

        self.heart_nudge     = pygame.Vector2(0, 0) * scale

        self.valuebar_spacing = (vb_h - int(vb_h * 0.7)) + (10 * scale)

        self.fill_inset    = pygame.Vector2(4, 4) * scale
        self.circle_offset = pygame.Vector2(-10, 0) * scale

        self.red_height  = 8 * scale
        self.blue_height = 6.5 * scale

        # ---- FX timers ----
        self._t = 0.0
        self._shake_timer = 0.0

    def set_values(
        self,
        hp: int,
        mana: int,
        max_hp: int | None = None,
        max_mana: int | None = None,
        mana_draining: bool = False,
        mana_regening: bool = False,
        mana_exhausted: bool = False,
    ):
        if max_hp is not None:
            self.max_hp = max(1, max_hp)
        if max_mana is not None:
            self.max_mana = max(1, max_mana)

        self.hp = max(0, min(hp, self.max_hp))
        self.mana = max(0, min(mana, self.max_mana))

        self.mana_draining = mana_draining
        self.mana_regening = mana_regening
        self.mana_exhausted = mana_exhausted

        # trigger shake when exhausted
        if mana_exhausted and not self._prev_exhausted:
            self._shake_timer = 0.18

        self._prev_exhausted = mana_exhausted

    def update(self, dt: float):
        self._t += dt
        if self._shake_timer > 0:
            self._shake_timer = max(0.0, self._shake_timer - dt)

    def _blit_fill(self, screen: pygame.Surface, img: pygame.Surface, topleft: tuple[int, int], ratio: float, height: int):
        ratio = max(0.0, min(1.0, ratio))
        w = int(img.get_width() * ratio)
        if w <= 0:
            return
        h = min(img.get_height(), int(height))
        part = img.subsurface(pygame.Rect(0, 0, w, h))
        screen.blit(part, topleft)

    def _apply_mana_fx(self, base_img: pygame.Surface) -> pygame.Surface:
        """Return a surface for mana fill with pulse / grayscale depending on state."""
        img = base_img

        if self.mana_exhausted:
            # grayscale / dim
            img = base_img.copy()
            img.fill((120, 120, 120), special_flags=pygame.BLEND_RGB_MULT)
            return img

        if self.mana_draining or self.mana_regening:
            # pulse alpha / brightness
            # draining = stronger pulse, regening = softer pulse
            strength = 110 if self.mana_draining else 70
            pulse = (math.sin(self._t * 10.0) + 1.0) * 0.5
            add = int(strength * pulse)

            img = base_img.copy()
            img.fill((15, 15, 15), special_flags=pygame.BLEND_RGB_ADD)  # tiny lift
            img.fill((add, add, add), special_flags=pygame.BLEND_RGB_ADD)  # pulse
            return img

        return img

    def draw(self, screen: pygame.Surface):
        # optional shake (only when exhausted)
        shake_x = 0
        shake_y = 0
        if self._shake_timer > 0:
            # small deterministic shake (no random)
            shake_x = int(math.sin(self._t * 60.0) * 2)
            shake_y = int(math.cos(self._t * 60.0) * 1)

        base = self.pos + self.panel_offset + pygame.Vector2(shake_x, shake_y)
        x, y = int(base.x), int(base.y)

        # positions
        vb1_pos = (
            x + int(self.valuebar_offset.x + self.hp_bar_nudge.x),
            y + int(self.valuebar_offset.y + self.hp_bar_nudge.y),
        )

        vb2_pos = (
            vb1_pos[0] + int(self.mana_bar_nudge.x),
            vb1_pos[1] + int(self.valuebar_spacing) + int(self.mana_bar_nudge.y),
        )

        hp_ratio = 0.0 if self.max_hp <= 0 else (self.hp / self.max_hp)
        mana_ratio = 0.0 if self.max_mana <= 0 else (self.mana / self.max_mana)

        hp_fill_pos = (
            vb1_pos[0] + int(self.fill_inset.x + self.hp_fill_nudge.x),
            vb1_pos[1] + int(self.fill_inset.y + self.hp_fill_nudge.y),
        )

        mana_fill_pos = (
            vb2_pos[0] + int(self.fill_inset.x + self.mana_fill_nudge.x),
            vb2_pos[1] + int(self.fill_inset.y + self.mana_fill_nudge.y),
        )

        # HP
        self._blit_fill(screen, self.red, hp_fill_pos, hp_ratio, self.red_height)
        screen.blit(self.valuebar, vb1_pos)

        # MANA (with FX)
        blue_fx = self._apply_mana_fx(self.blue)
        self._blit_fill(screen, blue_fx, mana_fill_pos, mana_ratio, self.blue_height)
        screen.blit(self.mana_valuebar, vb2_pos)

        # circle
        cpos = (
            x + int(self.circle_offset.x + self.circle_nudge.x),
            y + int(self.circle_offset.y + self.circle_nudge.y),
        )
        screen.blit(self.circle, cpos)

        # heart (center in circle)
        circle_rect = self.circle.get_rect(topleft=cpos)
        heart_rect = self.heart.get_rect(center=circle_rect.center)
        heart_rect.x += int(self.heart_nudge.x)
        heart_rect.y += int(self.heart_nudge.y)
        screen.blit(self.heart, heart_rect)