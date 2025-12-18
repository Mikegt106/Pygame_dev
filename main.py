import pygame
from entities import Player
from enemies import Zombie
from config import PLAYER, PROJECTILES, ZOMBIE, DAMAGE
from ui_statbar import StatBarUI
from spawner import EnemySpawner

pygame.init()
font = pygame.font.SysFont(None, 36)
font_big = pygame.font.SysFont(None, 120)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

statui = StatBarUI()

WORLD_WIDTH = 6000

spawner = EnemySpawner(
    enemy_cls=Zombie,
    enemy_cfg=ZOMBIE,
    spawn_y=680,
    interval_min=1.2,
    interval_max=2.5,
    max_enemies=6,
    min_dist_from_player=250,
    spawn_ahead_min=400,
    spawn_ahead_max=900,
    spawn_behind_chance=0.20,
)

def reset_game():
    spawner.reset()
    player = Player(640, 680, PLAYER)
    projectiles = []
    zombies = []
    return player, projectiles, zombies

player, projectiles, zombies = reset_game()

running = True
while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            player, projectiles, zombies = reset_game()

    keys = pygame.key.get_pressed()

    if not player.dead:
        player.update(keys, dt, projectiles, PROJECTILES)

        # spawn
        spawner.update(dt, player, zombies, world_width=WORLD_WIDTH)

        # enemies update
        for z in zombies:
            z.update(dt, player)

        # projectiles update
        for p in projectiles:
            p.update(dt)

        # collisions
        for p in projectiles:
            for z in zombies:
                if p.rect.colliderect(z.rect) and (not z.dead):
                    z.take_damage(DAMAGE["book"])
                    p.age = p.lifetime

        projectiles = [p for p in projectiles if not p.is_dead()]

        # remove zombies that finished dying
        zombies = [z for z in zombies if not getattr(z, "remove", False)]

    else:
        player.update(keys, dt, projectiles, PROJECTILES)

    # UI
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

    # DRAW
    screen.fill((20, 20, 20))
    statui.draw(screen)
    player.draw(screen)
    for z in zombies:
        z.draw(screen)
    for p in projectiles:
        p.draw(screen)

    if player.dead:
        text = font_big.render("YOU DIED", True, (255, 255, 255))
        rect = text.get_rect(center=(1280 // 2, 120))
        screen.blit(text, rect)
        tip = font.render("Press R to respawn", True, (255, 255, 255))
        screen.blit(tip, (20, 60))

    pygame.display.flip()

pygame.quit()