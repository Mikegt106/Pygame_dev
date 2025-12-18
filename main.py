import pygame
import config
import entities.enemies  # IMPORTANT: registreert enemy classes

from entities import Player
from ui_statbar import StatBarUI
from spawner import EnemySpawner
from wave_system import WaveSystem

pygame.init()
font = pygame.font.SysFont(None, 36)
font_big = pygame.font.SysFont(None, 120)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

WORLD_WIDTH = 6000
statui = StatBarUI()

spawner = EnemySpawner(
    pool=config.ENEMY_POOL,
    cfg_module=config,
    spawn_y=680,
    interval_min=1.2,
    interval_max=2.5,
    max_enemies=6,
)

wave_sys = WaveSystem(break_time=4.0, fight_time=18.0)
wave_sys.start()

def reset_game():
    spawner.reset()
    wave_sys.start()
    player = Player(640, 680, config.PLAYER)
    projectiles = []
    enemies = []
    return player, projectiles, enemies

player, projectiles, enemies = reset_game()

running = True
while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            player, projectiles, enemies = reset_game()

    keys = pygame.key.get_pressed()

    # wave update (past spawner settings aan)
    wave_sys.update(dt, spawner)

    if not player.dead:
        player.update(keys, dt, projectiles, config.PROJECTILES)

        # spawn alleen tijdens fight
        if wave_sys.is_fight():
            spawner.update(dt, player, enemies, world_width=WORLD_WIDTH)

        # enemies
        for e in enemies:
            e.update(dt, player)

        # projectiles
        for p in projectiles:
            p.update(dt)

        # collisions
        for p in projectiles:
            for e in enemies:
                if p.rect.colliderect(e.rect) and (not getattr(e, "dead", False)):
                    e.take_damage(config.DAMAGE["book"])
                    p.age = p.lifetime

        projectiles = [p for p in projectiles if not p.is_dead()]
        enemies = [e for e in enemies if not getattr(e, "remove", False)]

    else:
        player.update(keys, dt, projectiles, config.PROJECTILES)

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

    wave_text = font.render(f"WAVE {wave_sys.wave} - {wave_sys.state}", True, (255, 255, 255))
    screen.blit(wave_text, (95, 10))

    statui.draw(screen)
    player.draw(screen)

    for e in enemies:
        e.draw(screen)

    for p in projectiles:
        p.draw(screen)

    if player.dead:
        text = font_big.render("YOU DIED", True, (255, 255, 255))
        rect = text.get_rect(center=(1280 // 2, 120))
        screen.blit(text, rect)
        # (geen respawn tip meer)

    pygame.display.flip()

pygame.quit()