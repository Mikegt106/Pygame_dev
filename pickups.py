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

        # bobbing
        self.bob_timer = random.uniform(0, 6.28)
        self.base_y = None          # zetten we pas correct NA landing
        self.on_ground = False

        # --------- LOAD IMAGES ONCE ----------
        if CoinPickup.COIN_SMALL is None:
            CoinPickup.COIN_SMALL = pygame.transform.scale(
                load_image("assets/Items/Coin.png", alpha=True), (22, 22)
            )

        if CoinPickup.COIN_MED is None:
            CoinPickup.COIN_MED = pygame.transform.scale(
                load_image("assets/Items/Copper.png", alpha=True), (26, 26)
            )

        if CoinPickup.COIN_BIG is None:
            CoinPickup.COIN_BIG = pygame.transform.scale(
                load_image("assets/Items/Silver.png", alpha=True), (30, 30)
            )

        # --------- PICK IMAGE BY VALUE ----------
        if self.value >= 10:
            self.image = CoinPickup.COIN_BIG
        elif self.value >= 5:
            self.image = CoinPickup.COIN_MED
        else:
            self.image = CoinPickup.COIN_SMALL

        self.rect = self.image.get_rect(center=(int(x), int(y)))

        # --------- DROP PHYSICS ----------
        self.vx = random.uniform(-40, 40)
        self.vy = random.uniform(-60, -20)
        self.gravity = 600.0

        self.age = 0.0
        self.lifetime = 12.0

    def update(self, dt: float):
        if self.collected:
            return

        self.age += dt

        # --------- PHYSICS ----------
        if not self.on_ground:
            self.vy += self.gravity * dt
            self.rect.x += int(self.vx * dt)
            self.rect.y += int(self.vy * dt)
            self.vx *= 0.98

            ground_y = 680
            if self.rect.bottom >= ground_y:
                self.rect.bottom = ground_y

                # bounce (iets sterker)
                self.vy *= -0.55
                self.vx *= 0.6

                # settle
                if abs(self.vy) < 25:
                    self.vy = 0
                    self.gravity = 0      # 🔑 stop physics volledig
                    self.on_ground = True
                    self.base_y = self.rect.y

        # --------- BOBBING (alleen als stil) ----------
        if self.on_ground:
            self.bob_timer += dt * 3
            self.rect.y = self.base_y + int(4 * math.sin(self.bob_timer))

    def collect(self):
        self.collected = True

    def is_dead(self) -> bool:
        return self.collected or (self.age >= self.lifetime)

    def draw(self, screen: pygame.Surface):
        if not self.collected:
            screen.blit(self.image, self.rect)