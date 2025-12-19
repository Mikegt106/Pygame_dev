# ui/menu_ui.py
import pygame


class MenuUI:
    def __init__(self, screen: pygame.Surface, scale: float = 1.6, margin: int = 24, spacing: int = 10):
        self.screen = screen
        self.scale = float(scale)
        self.margin = int(margin)
        self.spacing = int(spacing * self.scale)

        # -------------------------
        # load + scale assets
        # -------------------------
        box_raw = pygame.image.load("assets/MenuUI/MenuBox.png").convert_alpha()
        icon_paths = [
            "assets/MenuUI/Backpack.png",
            "assets/MenuUI/Profile.png",
            "assets/MenuUI/Settings.png",
        ]

        self.box = pygame.transform.scale(
            box_raw,
            (int(box_raw.get_width() * self.scale), int(box_raw.get_height() * self.scale))
        )

        self.icons = []
        for p in icon_paths:
            img = pygame.image.load(p).convert_alpha()
            self.icons.append(
                pygame.transform.scale(
                    img,
                    (int(img.get_width() * self.scale), int(img.get_height() * self.scale))
                )
            )

        self.box_w = self.box.get_width()
        self.box_h = self.box.get_height()

        # -------------------------
        # position: top-right
        # -------------------------
        screen_w = self.screen.get_width()
        total_w = (3 * self.box_w) + (2 * self.spacing)

        self.x = screen_w - total_w - self.margin
        self.y = self.margin

        # clickable rects
        self.rects = []
        for i in range(3):
            bx = self.x + i * (self.box_w + self.spacing)
            by = self.y
            self.rects.append(pygame.Rect(bx, by, self.box_w, self.box_h))

    # -------------------------
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, r in enumerate(self.rects):
                if r.collidepoint(event.pos):
                    return i
        return None

    # -------------------------
    def draw(self):
        for i, icon in enumerate(self.icons):
            r = self.rects[i]

            # box
            self.screen.blit(self.box, r.topleft)

            # center icon
            ix = r.x + (r.width - icon.get_width()) // 2
            iy = r.y + (r.height - icon.get_height()) // 2
            self.screen.blit(icon, (ix, iy))