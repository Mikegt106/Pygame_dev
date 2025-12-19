# pickups.py
import random
import math
import pygame
from assets import load_image


class CoinPickup:
    COIN_SMALL = None
    COIN_MED = None
    COIN_BIG = None

    def __init__(self, x: float, y: float, value: int = 1):
        self.value = int(value)
        self.collected = False
        
        #Magenet drop
        self.magnet_speed = 900.0
        self.magnet_radius = 140
        self.pickup_radius = 22
        self.magnet_active = False

        # bobbing
        self.on_ground = False
        self.bob_timer = random.uniform(0, math.tau)
        self.base_y = int(y)

        # --------- LOAD IMAGES ONCE ----------
        scale_multiplier = 2
        if CoinPickup.COIN_SMALL is None:
            CoinPickup.COIN_SMALL = pygame.transform.scale(
                load_image("assets/Items/Coin.png", alpha=True), (22*scale_multiplier, 22*scale_multiplier)
            )
        if CoinPickup.COIN_MED is None:
            CoinPickup.COIN_MED = pygame.transform.scale(
                load_image("assets/Items/Copper.png", alpha=True), (26*scale_multiplier, 26*scale_multiplier)
            )
        if CoinPickup.COIN_BIG is None:
            CoinPickup.COIN_BIG = pygame.transform.scale(
                load_image("assets/Items/Silver.png", alpha=True), (26*scale_multiplier, 26*scale_multiplier)
            )

        # --------- PICK IMAGE BY VALUE ----------
        if self.value >= 10:
            self.image = CoinPickup.COIN_BIG
        elif self.value >= 5:
            self.image = CoinPickup.COIN_MED
        else:
            self.image = CoinPickup.COIN_SMALL

        self.rect = self.image.get_rect(center=(int(x), int(y)))
        self.base_y = self.rect.y

        # --------- DROP PHYSICS ----------
        self.vx = random.uniform(-60, 60)
        self.vy = random.uniform(-220, -120)
        self.gravity = 1200.0

        self.age = 0.0
        self.lifetime = 12.0

    def update(self, dt: float, player_pos: tuple[int, int]):
        if self.collected:
            return

        self.age += dt

        px, py = player_pos
        cx, cy = self.rect.center
        dx = px - cx
        dy = py - cy
        dist2 = dx * dx + dy * dy

        # --- MAGNET TRIGGER ---
        if dist2 <= (self.magnet_radius * self.magnet_radius):
            self.magnet_active = True

        # --- MAGNET MOTION ---
        if self.magnet_active:
            # target = midden van player
            tx, ty = player_pos
            cx, cy = self.rect.center

            dx = tx - cx
            dy = ty - cy
            dist2 = dx*dx + dy*dy

            # dichtbij genoeg -> collect
            if dist2 <= (self.pickup_radius * self.pickup_radius):
                self.collect()
                return

            dist = math.sqrt(dist2)
            # max stap per frame
            step = self.magnet_speed * dt

            # als we in 1 stap kunnen -> snap erop
            if dist <= step:
                self.rect.center = (tx, ty)
            else:
                nx = dx / dist
                ny = dy / dist
                self.rect.centerx += int(nx * step)
                self.rect.centery += int(ny * step)

            return

        # --- NORMAL DROP + BOUNCE ---
        if not self.on_ground:
            self.vy += self.gravity * dt
            self.rect.x += int(self.vx * dt)
            self.rect.y += int(self.vy * dt)
            self.vx *= 0.98

            ground_y = 680
            if self.rect.bottom >= ground_y:
                self.rect.bottom = ground_y

                # bounce
                self.vy *= -0.55
                self.vx *= 0.6

                # settle
                if abs(self.vy) < 30:
                    self.vy = 0.0
                    self.vx = 0.0
                    self.on_ground = True
                    self.base_y = self.rect.y

        # --- BOBBING (alleen als stil) ---
        if self.on_ground:
            self.bob_timer += dt * 3.0
            self.rect.y = self.base_y + int(4 * math.sin(self.bob_timer))

    def collect(self):
        self.collected = True

    def is_dead(self) -> bool:
        return self.collected or self.age >= self.lifetime

    def draw(self, screen: pygame.Surface):
        if not self.collected:
            screen.blit(self.image, self.rect)