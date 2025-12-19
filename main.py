# main.py
import pygame
import config
import entities.enemies  # IMPORTANT: registreert enemy classes

from entities import Player
from ui.ui_statbar import StatBarUI
from spawner import EnemySpawner
from wave_system import WaveSystem
from loot_system import LootSystem
from ui.menu_ui import MenuUI
from ui.inventory_ui import InventoryUI
from ui.main_screen import MainScreen
from dialogue.intro import get_intro_lines
from ui.dialogue_ui import DialogueUI
from ui.settings_menu import SettingsMenu

pygame.init()

# ----------------------------------
# BACKGROUND MUSIC
# ----------------------------------
pygame.mixer.init()
pygame.mixer.music.load("assets/Sounds/bg_music.mp3")
pygame.mixer.music.set_volume(0.35)
pygame.mixer.music.play(-1)

# SFX
school_bell = pygame.mixer.Sound("assets/Sounds/school_bell.mp3")
school_bell.set_volume(0.7)

# ----------------------------------
# FONTS MANAGEMENT
# ----------------------------------
font = pygame.font.SysFont(None, 36)
font_big = pygame.font.SysFont(None, 96)
font_small = pygame.font.SysFont(None, 24)

screen = pygame.display.set_mode((1280, 720))
scene_cache = {}
main_screen = MainScreen(screen)
state = "MAIN"
clock = pygame.time.Clock()

WORLD_WIDTH = 6000

# ✅ current scene persistence (fix voor “leeg scherm”)
current_scene = None

# ----------------------------------
# UI INITIALISATION
# ----------------------------------
statui = StatBarUI()
menu_ui = MenuUI(screen)
inventory_ui = InventoryUI(screen)
loot_sys = LootSystem()
dialogue_ui = DialogueUI(screen)
settings_menu = SettingsMenu(screen)

# ----------------------------------
# SYSTEM klaarzetten
# ----------------------------------
spawner = EnemySpawner(
    pool=config.ENEMY_POOL,
    cfg_module=config,
    spawn_y=680,
    interval_min=1.2,
    interval_max=2.5,
    max_enemies=6,
)

wave_sys = WaveSystem(waves=config.WAVES, break_time=4.0)
wave_sys.start()


def start_intro():
    global state
    dialogue_ui.start(get_intro_lines())
    state = "INTRO"


def reset_game():
    spawner.reset()
    wave_sys.start()
    player = Player(640, 680, config.PLAYER)
    projectiles = []
    enemies = []
    pickups = []
    return player, projectiles, enemies, pickups


player, projectiles, enemies, pickups = reset_game()


def draw_scene_background(path: str):
    if not path:
        screen.fill((20, 20, 20))
        return

    if path not in scene_cache:
        img = pygame.image.load(path).convert()
        img = pygame.transform.scale(img, screen.get_size())
        scene_cache[path] = img

    screen.blit(scene_cache[path], (0, 0))


def set_scene_for_wave(wave_nr: int):
    """Zet current_scene op basis van config.WAVES[wave_nr]['scene']."""
    global current_scene
    cfg = config.WAVES.get(wave_nr, {})
    scene = cfg.get("scene")
    if scene:
        current_scene = scene


# ----------------------------
# FADE-IN (na intro)
# ----------------------------
fade_alpha = 0
fade_speed = 320  # alpha per second
fade_surface = pygame.Surface(screen.get_size())
fade_surface.fill((0, 0, 0))

# ----------------------------------
# Actual running
# ----------------------------------
running = True
while running:
    dt = clock.tick(60) / 1000.0
    keys = pygame.key.get_pressed()
    ui_used_click_this_frame = False

    # --------------------------------------------------
    # EVENTS
    # --------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        # --- MAIN SCREEN ---
        if state == "MAIN":
            action = main_screen.handle_event(event)
            if action == "PLAY":
                start_intro()
            continue

        # --- INTRO (dialogue) ---
        if state == "INTRO":
            dialogue_ui.handle_event(event)

            if dialogue_ui.is_done():
                school_bell.play()
                set_scene_for_wave(1)   # bg klaar voor wave 1
                state = "FADEIN"
                fade_alpha = 255
            continue

        # --- IN-GAME EVENTS (PLAY) ---
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            if player.dead:
                player, projectiles, enemies, pickups = reset_game()

        used_ui, clicked = menu_ui.handle_event(event)
        if used_ui:
            ui_used_click_this_frame = True

            if clicked == 0:
                inventory_ui.toggle()
            elif clicked == 1:
                print("Profile clicked")
            elif clicked == 2:
                settings_menu.toggle()

        if hasattr(inventory_ui, "handle_event"):
            if inventory_ui.handle_event(event):
                ui_used_click_this_frame = True

        action = settings_menu.handle_event(event)
        if action == "resume":
            settings_menu.visible = False
        elif action == "restart":
            player, projectiles, enemies, pickups = reset_game()
            settings_menu.visible = False
        elif action == "menu":
            state = "MAIN"
            settings_menu.visible = False

    # --------------------------------------------------
    # STATE: MAIN
    # --------------------------------------------------
    if state == "MAIN":
        main_screen.update(dt)
        main_screen.draw()
        pygame.display.flip()
        continue

    # --------------------------------------------------
    # STATE: INTRO
    # --------------------------------------------------
    if state == "INTRO":
        screen.fill((10, 10, 10))
        dialogue_ui.update(dt)
        dialogue_ui.draw()
        pygame.display.flip()
        continue

    # --------------------------------------------------
    # STATE: FADEIN
    # --------------------------------------------------
    if state == "FADEIN":
        fade_alpha -= fade_speed * dt
        if fade_alpha <= 0:
            fade_alpha = 0
            state = "PLAY"

        draw_scene_background(current_scene)
        player.draw(screen)

        statui.draw(screen)
        menu_ui.draw()
        inventory_ui.draw()

        fade_surface.set_alpha(int(fade_alpha))
        screen.blit(fade_surface, (0, 0))

        pygame.display.flip()
        continue

    # --------------------------------------------------
    # PLAY: UI UPDATE (hover states)
    # --------------------------------------------------
    menu_ui.update()
    inventory_ui.update(dt)

    # --------------------------------------------------
    # PLAY: UI BLOCK INPUT
    # --------------------------------------------------
    mouse_pos = pygame.mouse.get_pos()
    ui_block_input = False

    if inventory_ui.visible and any(r.collidepoint(mouse_pos) for r in inventory_ui.rects):
        ui_block_input = True
    if any(r.collidepoint(mouse_pos) for r in menu_ui.rects):
        ui_block_input = True

    # settings menu = pause (blok input)
    paused = settings_menu.visible
    if paused:
        ui_block_input = True

    ui_block_input = ui_block_input or ui_used_click_this_frame

    # --------------------------------------------------
    # ✅ PLAY: GAMEPLAY UPDATE (alleen als NIET paused)
    # --------------------------------------------------
    if not paused:
        # wave
        wave_sys.update(dt, spawner, enemies)

        # player
        player.update(keys, dt, projectiles, config.PROJECTILES, ui_block_input)

        # keep player inside screen
        SW, SH = screen.get_size()
        MARGIN_X = 5
        if player.rect.centerx < MARGIN_X:
            player.rect.centerx = MARGIN_X
        if player.rect.centerx > SW - MARGIN_X:
            player.rect.centerx = SW - MARGIN_X

        # sync eventuele float-pos variabelen (als je Player die gebruikt)
        if hasattr(player, "pos"):
            try:
                player.pos.x = float(player.rect.centerx)
            except Exception:
                pass
        if hasattr(player, "x"):
            player.x = float(player.rect.centerx)

        # spawn
        if (not player.dead) and wave_sys.can_spawn():
            before = len(enemies)
            spawner.update(dt, player, enemies, world_width=WORLD_WIDTH)
            spawned_now = len(enemies) - before
            if spawned_now > 0:
                wave_sys.on_spawned(spawned_now)

        # enemies / projectiles
        for e in enemies:
            e.update(dt, player)
        for p in projectiles:
            p.update(dt)

        # pickups
        for c in pickups:
            was_collected = getattr(c, "collected", False)
            c.update(dt, player)
            if (not was_collected) and getattr(c, "collected", False):
                player.coins = getattr(player, "coins", 0) + getattr(c, "value", 1)

        # collisions
        for p in projectiles:
            for e in enemies:
                if p.rect.colliderect(e.rect) and not getattr(e, "dead", False):
                    e.take_damage(config.DAMAGE["book"])
                    p.age = p.lifetime

        # loot
        for e in enemies:
            if getattr(e, "dead", False) and not getattr(e, "_loot_dropped", False):
                loot_sys.on_enemy_death(e, pickups)

        # cleanup
        projectiles = [p for p in projectiles if not p.is_dead()]
        enemies = [e for e in enemies if not getattr(e, "remove", False)]
        pickups = [c for c in pickups if not getattr(c, "remove", False) and not c.is_dead()]

    # --------------------------------------------------
    # UI UPDATE (mag ook tijdens pause, toont HP/coins etc.)
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
    current_wave_cfg = config.WAVES.get(wave_sys.wave, {})
    scene = current_wave_cfg.get("scene") or current_scene
    current_scene = scene
    draw_scene_background(scene)

    wave_text = font.render(f"WAVE {wave_sys.wave} - {wave_sys.state}", True, (255, 255, 255))
    screen.blit(wave_text, (100, 10))

    remaining = max(0, (wave_sys.spawn_limit - wave_sys.spawned) + len(enemies))
    left_text = font_small.render(f"ENEMIES LEFT: {remaining}", True, (255, 255, 255))
    screen.blit(left_text, (100, 80))

    if wave_sys.toast_text:
        toast = font_big.render(wave_sys.toast_text, True, (255, 255, 255))
        toast = toast.convert_alpha()
        toast.set_alpha(wave_sys.get_toast_alpha())
        rect = toast.get_rect(center=(1280 // 2, 120))
        screen.blit(toast, rect)

    player.draw(screen)

    for e in enemies:
        e.draw(screen)
    for p in projectiles:
        p.draw(screen)
    for c in pickups:
        c.draw(screen)

    coin_text = font_small.render(f"COINS: {getattr(player, 'coins', 0)}", True, (255, 255, 0))
    screen.blit(coin_text, (100, 105))

    # UI boven alles
    statui.draw(screen)
    menu_ui.draw()
    inventory_ui.draw()
    settings_menu.draw()

    if player.dead:
        text = font_big.render("YOU DIED", True, (255, 255, 255))
        rect = text.get_rect(center=(1280 // 2, 120))
        screen.blit(text, rect)

    pygame.display.flip()

pygame.quit()