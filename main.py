import pygame
from entities import Player
from enemies import Zombie
from config import PLAYER, PROJECTILES, ZOMBIE, DAMAGE

pygame.init()
font = pygame.font.SysFont(None, 36)
font_big = pygame.font.SysFont(None, 120)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

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

        # respawn
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            player, projectiles, zombies = reset_game()

    keys = pygame.key.get_pressed()

    # Alleen gameplay updates als je niet dood bent
    if not player.dead:
        player.update(keys, dt, projectiles, PROJECTILES)

        for p in projectiles:
            p.update(dt)

        for z in zombies:
            z.update(dt, player)

        # projectile -> zombie hit
        for p in projectiles:
            for z in zombies:
                if p.rect.colliderect(z.rect) and not z.dead:
                    z.take_damage(DAMAGE["book"])
                    p.age = p.lifetime

        projectiles = [p for p in projectiles if not p.is_dead()]
    else:
        # laat death anim nog doorlopen (als je die in player.update doet)
        player.update(keys, dt, projectiles, PROJECTILES)

    # draw
    screen.fill((20, 20, 20))
    player.draw(screen)
    for z in zombies:
        z.draw(screen)
    for p in projectiles:
        p.draw(screen)

    hp_text = font.render(f"HP: {player.hp}", True, (255, 255, 255))
    screen.blit(hp_text, (20, 20))

    if player.dead:
        text = font_big.render("YOU DIED", True, (255, 255, 255))
        rect = text.get_rect(center=(1280 // 2, 120))
        screen.blit(text, rect)

        tip = font.render("Press R to respawn", True, (255, 255, 255))
        screen.blit(tip, (20, 60))

    pygame.display.flip()

pygame.quit()