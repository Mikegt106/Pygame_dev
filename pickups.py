# pickups.py
import random
import math
import pygame
from assets import load_image


def _scale_image(img: pygame.Surface, scale: float) -> pygame.Surface:
    scale = float(scale)
    if scale == 1.0:
        return img
    w, h = img.get_size()
    nw, nh = max(1, int(w * scale)), max(1, int(h * scale))
    return pygame.transform.smoothscale(img, (nw, nh))


# ==========================================================
# COIN PICKUP SOUND
# ==========================================================
pygame.mixer.init()

COIN_SOUND = pygame.mixer.Sound("assets/Sounds/coins.mp3")
COIN_SOUND.set_volume(0.6)


# ==========================================================
# BASE PICKUP (magnet + drop physics + bobbing)
# ==========================================================
class BasePickup:
    def __init__(
        self,
        x: float,
        y: float,
        image: pygame.Surface,
        *,
        scale: float = 1.0,          # ✅ nieuw
        ground_y: int = 680,
        lifetime: float = 12.0,
        magnet_speed: float = 900.0,
        magnet_radius: int = 140,
        pickup_radius: int = 22,
    ):
        self.image = _scale_image(image, scale)  # ✅ schaal hier
        self.rect = self.image.get_rect(center=(int(x), int(y)))

        # state
        self.collected = False
        self.remove = False  # compat met je cleanup

        # magnet
        self.magnet_speed = float(magnet_speed)
        self.magnet_radius = int(magnet_radius)

        # ✅ pickup radius mee laten schalen (voelt beter bij grote items)
        self.pickup_radius = int(pickup_radius * float(scale))
        self.magnet_active = False

        # physics
        self.ground_y = int(ground_y)
        self.vx = random.uniform(-60, 60)
        self.vy = random.uniform(-220, -120)
        self.gravity = 1200.0
        self.on_ground = False

        # bobbing
        self.bob_timer = random.uniform(0, math.tau)
        self.base_y = self.rect.y

        # lifetime
        self.age = 0.0
        self.lifetime = float(lifetime)

    # ---------
    # hooks
    # ---------
    def apply(self, player):
        """Override in child classes."""
        pass

    def collect(self, player):
        """Unified collect: mark + apply + remove."""
        if self.collected:
            return
        self.collected = True
        self.apply(player)
        self.remove = True

    # ---------
    # common update
    # ---------
    def update(self, dt: float, player):
        if self.collected:
            return

        self.age += dt

        px, py = player.rect.midbottom
        cx, cy = self.rect.center
        dx = px - cx
        dy = py - cy
        dist2 = dx * dx + dy * dy

        # magnet trigger
        if dist2 <= (self.magnet_radius * self.magnet_radius):
            self.magnet_active = True

        # magnet motion
        if self.magnet_active:
            # dichtbij genoeg -> collect
            if dist2 <= (self.pickup_radius * self.pickup_radius):
                self.collect(player)
                return

            dist = math.sqrt(dist2)
            step = self.magnet_speed * dt

            if dist <= step:
                self.rect.center = (px, py)
            else:
                self.rect.centerx += int(dx / dist * step)
                self.rect.centery += int(dy / dist * step)
            return

        # drop physics
        if not self.on_ground:
            self.vy += self.gravity * dt
            self.rect.x += int(self.vx * dt)
            self.rect.y += int(self.vy * dt)
            self.vx *= 0.98

            if self.rect.bottom >= self.ground_y:
                self.rect.bottom = self.ground_y

                # bounce
                self.vy *= -0.55
                self.vx *= 0.6

                # settle
                if abs(self.vy) < 30:
                    self.vy = 0.0
                    self.vx = 0.0
                    self.on_ground = True
                    self.base_y = self.rect.y

        # bobbing (alleen als stil)
        if self.on_ground:
            self.bob_timer += dt * 3.0
            self.rect.y = self.base_y + int(4 * math.sin(self.bob_timer))

    def is_dead(self):
        return self.remove or self.age >= self.lifetime

    def draw(self, screen: pygame.Surface):
        if not self.collected:
            screen.blit(self.image, self.rect)


# ==========================================================
# COIN PICKUP
# ==========================================================
class CoinPickup(BasePickup):
    COIN_SMALL = None
    COIN_MED = None
    COIN_BIG = None

    def __init__(self, x: float, y: float, value: int = 1):
        self.value = int(value)

        # images cached
        scale = 2
        if CoinPickup.COIN_SMALL is None:
            CoinPickup.COIN_SMALL = pygame.transform.scale(
                load_image("assets/Items/Coin.png", alpha=True), (22 * scale, 22 * scale)
            )
        if CoinPickup.COIN_MED is None:
            CoinPickup.COIN_MED = pygame.transform.scale(
                load_image("assets/Items/Copper.png", alpha=True), (26 * scale, 26 * scale)
            )
        if CoinPickup.COIN_BIG is None:
            CoinPickup.COIN_BIG = pygame.transform.scale(
                load_image("assets/Items/Silver.png", alpha=True), (26 * scale, 26 * scale)
            )

        if self.value >= 10:
            img = CoinPickup.COIN_BIG
        elif self.value >= 5:
            img = CoinPickup.COIN_MED
        else:
            img = CoinPickup.COIN_SMALL

        super().__init__(x, y, img)  # coins al geschaald via cached images

    def apply(self, player):
        player.coins = getattr(player, "coins", 0) + self.value
        
    def collect(self, player):
        if self.collected:
            return
        
        COIN_SOUND.play()

        self.collected = True
        self.apply(player)
        self.remove = True


# ==========================================================
# ITEM PICKUP (Apple, Potion, etc.)
# ==========================================================
class ItemPickup(BasePickup):
    def __init__(self, x: float, y: float, cfg: dict):
        self.item_id = cfg["id"]          # bv "APPLE"
        self.amount = int(cfg.get("amount", 1))

        img = pygame.image.load(cfg["image"]).convert_alpha()

        # ✅ groter maken (tweakbaar per item via config: drop_scale)
        drop_scale = float(cfg.get("drop_scale", 2.2))

        super().__init__(x, y, img, scale=drop_scale)

    def apply(self, player):
        player.add_item(self.item_id, self.amount)