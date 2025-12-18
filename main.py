import pygame
from entities import Player
from enemies import Zombie
from config import PLAYER, PROJECTILES, ZOMBIE, DAMAGE
from ui_statbar import StatBarUI
from spawner import EnemySpawner

# -------------------------------------------------
# INIT
# -------------------------------------------------
pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 36)
font_big = pygame.font.SysFont(None, 120)

statui = StatBarUI()

WORLD_WIDTH = 6000

# -------------------------------------------------
# SPAWNER
# -------------------------------------------------
spawner = EnemySpawner(
    enemy_cfg=ZOMBIE,
    spawn_y=680,
    interval_min=1.2,
    interval_max=2.5,
    max_enemies=6,
)

# -------------------------------------------------
# RESET
# -------------------------------------------------
def reset_game():
    player = Player(640, 680, PLAYER)
    projectiles = []
    zombies = []
    spawner.reset()
    return player, projectiles, zombies


player, projectiles, zombies = reset_game()

# -------------------------------------------------
# MAIN LOOP
# -------------------------------------------------
running = True
while running:
    dt = clock.tick(60) / 1000.0

    # ---------------- EVENTS ----------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            player, projectiles, zombies = reset_game()

    keys = pygame.key.get_pressed()

    # ---------------- UPDATE ----------------
    if not player.dead:
        player.update(keys, dt, projectiles, PROJECTILES)

        # spawn enemies
        spawner.update(dt, player, zombies, world_width=WORLD_WIDTH)

        # update enemies
        for z in zombies:
            z.update(dt, player)

        # update projectiles
        for p in projectiles:
            p.update(dt)

        # collisions
        for p in projectiles:
            for z in zombies:
                if not z.dead and p.rect.colliderect(z.rect):
                    z.take_damage(DAMAGE["book"])
                    p.age = p.lifetime

        # cleanup projectiles
        projectiles = [p for p in projectiles if not p.is_dead()]

        # cleanup zombies (pas NA dead anim)
        zombies = [z for z in zombies if not z.remove]

    else:
        # laat player dead anim doorlopen
        player.update(keys, dt, projectiles, PROJECTILES)

    # ---------------- UI ----------------
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

    # ---------------- DRAW ----------------
    screen.fill((20, 20, 20))

    player.draw(screen)

    for z in zombies:
        z.draw(screen)

    for p in projectiles:
        p.draw(screen)

    statui.draw(screen)

    if player.dead:
        text = font_big.render("YOU DIED", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=(640, 120)))

        tip = font.render("Press R to respawn", True, (255, 255, 255))
        screen.blit(tip, (20, 60))

    pygame.display.flip()

pygame.quit()