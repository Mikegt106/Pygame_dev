import pygame
from entities import Player
from enemies import Zombie
from config import PLAYER, PROJECTILES, ZOMBIE, DAMAGE
from ui_statbar import StatBarUI

pygame.init()
font = pygame.font.SysFont(None, 36)
font_big = pygame.font.SysFont(None, 120)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

# ✅ maak UI pas na pygame.init()
statui = StatBarUI()

def reset_game():
    player = Player(640, 680, PLAYER)
    projectiles = []
    zombies = [Zombie(300, 680, ZOMBIE)]
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

        for p in projectiles:
            p.update(dt)

        for z in zombies:
            z.update(dt, player)

        for p in projectiles:
            for z in zombies:
                if p.rect.colliderect(z.rect) and not z.dead:
                    z.take_damage(DAMAGE["book"])
                    p.age = p.lifetime

        projectiles = [p for p in projectiles if not p.is_dead()]
    else:
        player.update(keys, dt, projectiles, PROJECTILES)

    # ✅ update bar values (mana later uit player)
    statui.set_values(player.hp, 50, max_hp=PLAYER.get("hp", 10), max_mana=50)

    # draw
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