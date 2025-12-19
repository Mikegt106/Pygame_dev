# ui/main_screen.py
import pygame


class MainScreen:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.w, self.h = screen.get_size()

        # -------- ASSETS --------
        self.bg = pygame.image.load(
            "assets/Mainscreen/Main_bg.png"
        ).convert()

        # scale naar scherm
        self.bg = pygame.transform.scale(self.bg, (self.w, self.h))

        # overlay voor contrast
        self.overlay = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 120))  # alpha = donkerder

        # fonts
        self.title_font = pygame.font.SysFont(None, 96)
        self.btn_font = pygame.font.SysFont(None, 40)
        self.small_font = pygame.font.SysFont(None, 26)

        # button rect
        bw, bh = 260, 70
        cx = self.w // 2
        cy = int(self.h * 0.62)

        self.play_rect = pygame.Rect(cx - bw // 2, cy, bw, bh)

        self.hover_play = False

    # -------------------------
    def update(self, dt: float):
        mx, my = pygame.mouse.get_pos()
        self.hover_play = self.play_rect.collidepoint((mx, my))

    # -------------------------
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.play_rect.collidepoint(event.pos):
                return "PLAY"

        if event.type == pygame.KEYDOWN:
            # optioneel: enter of space start game
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return "PLAY"

        return None

    # -------------------------
    def draw(self):
        # background
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.overlay, (0, 0))

        # title
        title = self.title_font.render("Quiet Before the Bell", True, (255, 255, 255))
        tr = title.get_rect(center=(self.w // 2, int(self.h * 0.28)))
        self.screen.blit(title, tr)

        subtitle = self.small_font.render(
            "The Silence Doesn’t Last",
            True,
            (220, 220, 220),
        )
        sr = subtitle.get_rect(center=(self.w // 2, int(self.h * 0.36)))
        self.screen.blit(subtitle, sr)

        # play button
        color = (80, 80, 80) if self.hover_play else (50, 50, 50)
        pygame.draw.rect(self.screen, color, self.play_rect, border_radius=14)
        pygame.draw.rect(self.screen, (255, 255, 255), self.play_rect, 2, border_radius=14)

        label = self.btn_font.render("PLAY", True, (255, 255, 255))
        lr = label.get_rect(center=self.play_rect.center)
        self.screen.blit(label, lr)