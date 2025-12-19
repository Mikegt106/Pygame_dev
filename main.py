# main.py
import pygame
import config
import entities.enemies  # IMPORTANT: registreert enemy classes

from entities import Player
from ui_statbar import StatBarUI
from spawner import EnemySpawner
from wave_system import WaveSystem
from loot_system import LootSystem

pygame.init()

font = pygame.font.SysFont(None, 36)
font_big = pygame.font.SysFont(None, 96)
font_small = pygame.font.SysFont(None, 24)

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

WORLD_WIDTH = 6000

statui = StatBarUI()
loot_sys = LootSystem(coins_min=0, coins_max=4)

# --------------------------------------------------
# SPAWNER (wordt per wave aangepast)
# --------------------------------------------------
spawner = EnemySpawner(
    pool=config.ENEMY_POOL,   # startpool (overschreven door waves)
    cfg_module=config,
    spawn_y=680,
    interval_min=1.2,
    interval_max=2.5,
    max_enemies=6,
)

# --------------------------------------------------
# WAVE SYSTEM
# --------------------------------------------------
wave_sys = WaveSystem(
    waves=config.WAVES,
    break_time=4.0
)
wave_sys.start()

# --------------------------------------------------
# RESET
# --------------------------------------------------
def reset_game():
    spawner.reset()
    wave_sys.start()

    player = Player(640, 680, config.PLAYER)
    projectiles = []
    enemies = []
    pickups = []
    return player, projectiles, enemies, pickups

player, projectiles, enemies, pickups = reset_game()

running = True
while running:
    dt = clock.tick(60) / 1000.0

    # --------------------------------------------------
    # EVENTS
    # --------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            player, projectiles, enemies, pickups = reset_game()  # ✅ pickups ook resetten

    keys = pygame.key.get_pressed()

    # --------------------------------------------------
    # WAVE UPDATE (stuurt spawner)
    # --------------------------------------------------
    wave_sys.update(dt, spawner, enemies)

    # --------------------------------------------------
    # PLAYER UPDATE (ALTIJD)
    # --------------------------------------------------
    player.update(keys, dt, projectiles, config.PROJECTILES)

    # --------------------------------------------------
    # SPAWN (max 1x per frame)
    # --------------------------------------------------
    if (not player.dead) and wave_sys.can_spawn():
        before = len(enemies)
        spawner.update(dt, player, enemies, world_width=WORLD_WIDTH)
        spawned_now = len(enemies) - before
        if spawned_now > 0:
            wave_sys.on_spawned(spawned_now)

    # --------------------------------------------------
    # ENEMIES UPDATE
    # --------------------------------------------------
    for e in enemies:
        e.update(dt, player)

    # --------------------------------------------------
    # PROJECTILES UPDATE
    # --------------------------------------------------
    for p in projectiles:
        p.update(dt)

    # --------------------------------------------------
    # PICKUPS UPDATE  ✅
    # --------------------------------------------------
    for c in pickups:
        was_collected = getattr(c, "collected", False)
        c.update(dt, player.rect.midbottom)

        # als hij net collected is geworden -> coins adden 1x
        if (not was_collected) and getattr(c, "collected", False):
            player.coins = getattr(player, "coins", 0) + getattr(c, "value", 1)

        PICKUP_DIST = 22 

        px, py = player.rect.midbottom
        cx, cy = c.rect.center

        dx = px - cx
        dy = py - cy

        if (dx*dx + dy*dy) <= (PICKUP_DIST * PICKUP_DIST):
            player.coins = getattr(player, "coins", 0) + getattr(c, "value", 1)
            c.dead = True
            continue

    # --------------------------------------------------
    # COLLISIONS (projectiles -> enemies)
    # --------------------------------------------------
    for p in projectiles:
        for e in enemies:
            if p.rect.colliderect(e.rect) and not getattr(e, "dead", False):
                e.take_damage(config.DAMAGE["book"])
                p.age = p.lifetime

    # --------------------------------------------------
    # LOOT DROPS (enemy net gestorven) ✅
    # --------------------------------------------------
    for e in enemies:
        if getattr(e, "dead", False) and not getattr(e, "_loot_dropped", False):
            loot_sys.on_enemy_death(e, pickups)

    # --------------------------------------------------
    # CLEANUP ✅
    # --------------------------------------------------
    projectiles = [p for p in projectiles if not p.is_dead()]
    enemies = [e for e in enemies if not getattr(e, "remove", False)]
    pickups = [c for c in pickups if not getattr(c, "dead", False) and not getattr(c, "remove", False)]

    # --------------------------------------------------
    # UI UPDATE
    # --------------------------------------------------
    statui.set_values(
        hp=player.hp,
        mana=int(player.mana),
        max_hp=player.max_hp,
        max_mana=int(player.max_mana),
        mana_draining=player.mana_draining,
        mana_regening=player.mana_regening,
        mana_exhausted=player.mana_exhausted,
    )
    statui.update(dt)

    # --------------------------------------------------
    # DRAW
    # --------------------------------------------------
    screen.fill((20, 20, 20))

    # --- Wave label ---
    wave_text = font.render(
        f"WAVE {wave_sys.wave} - {wave_sys.state}",
        True,
        (255, 255, 255),
    )
    screen.blit(wave_text, (100, 10))

    # --- Enemies left ---
    remaining = max(
        0,
        (wave_sys.spawn_limit - wave_sys.spawned) + len(enemies),
    )
    left_text = font_small.render(
        f"ENEMIES LEFT: {remaining}",
        True,
        (255, 255, 255),
    )
    screen.blit(left_text, (100, 80))

    # --- Wave cleared toast ---
    if wave_sys.toast_text:
        toast = font_big.render(wave_sys.toast_text, True, (255, 255, 255))
        toast = toast.convert_alpha()
        toast.set_alpha(wave_sys.get_toast_alpha())
        rect = toast.get_rect(center=(1280 // 2, 120))
        screen.blit(toast, rect)

    statui.draw(screen)
    player.draw(screen)

    for e in enemies:
        e.draw(screen)

    for p in projectiles:
        p.draw(screen)

    # pickups tekenen
    for c in pickups:
        c.draw(screen)
                
    coin_text = font_small.render(f"COINS: {getattr(player, 'coins', 0)}", True, (255, 255, 0))
    screen.blit(coin_text, (100, 105))

    if player.dead:
        text = font_big.render("YOU DIED", True, (255, 255, 255))
        rect = text.get_rect(center=(1280 // 2, 120))
        screen.blit(text, rect)

    pygame.display.flip()

pygame.quit()