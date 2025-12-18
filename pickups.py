# pickups.py
import random
import pygame
from assets import load_image  # jij hebt dit al in animation.py -> same helper

class CoinPickup:
    COIN_IMG = None

    def __init__(self, x: float, y: float, value: int = 1):
        self.value = int(value)

        if CoinPickup.COIN_IMG is None:
            img = load_image("assets/Items/Coin.png", alpha=True)
            CoinPickup.COIN_IMG = pygame.transform.scale(img, (22, 22))  # tweak size

        self.image = CoinPickup.COIN_IMG
        self.rect = self.image.get_rect(center=(int(x), int(y)))

        self.vx = random.uniform(-40, 40)
        self.vy = random.uniform(-60, -20)
        self.gravity = 600.0

        self.age = 0.0
        self.lifetime = 12.0

    def update(self, dt: float):
        self.age += dt
        self.vy += self.gravity * dt
        self.rect.x += int(self.vx * dt)
        self.rect.y += int(self.vy * dt)
        self.vx *= 0.98

        ground_y = 680
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.vy = 0.0

    def is_dead(self) -> bool:
        return self.age >= self.lifetime

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)