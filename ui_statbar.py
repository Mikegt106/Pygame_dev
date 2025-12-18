import pygame
from assets import load_image

class StatBarUI:
    def __init__(self, pos=(60, 20), scale=1.8):
        self.pos = pygame.Vector2(pos)
        self.scale = scale

        # load + scale once (via cached loader)
        self.panel    = load_image("assets/HealthbarUI/HealthBarPanel_160x41.png", alpha=True, scale=scale)
        self.circle   = load_image("assets/HealthbarUI/BlackBigCircleBoxWithBorder_27x27.png", alpha=True, scale=scale*1.2)
        self.valuebar = load_image("assets/HealthbarUI/ValueBar_128x16.png", alpha=True, scale=scale)
        self.red      = load_image("assets/HealthbarUI/ValueRed_120x8.png", alpha=True, scale=scale)
        self.blue     = load_image("assets/HealthbarUI/ValueBlue_120x8.png", alpha=True, scale=scale)
        self.knot     = load_image("assets/HealthbarUI/CornerKnot_14x14.png", alpha=True, scale=scale)

        # ✅ mana container = dezelfde valuebar maar dunner in HEIGHT (breedte blijft identiek)
        vb_w = self.valuebar.get_width()
        vb_h = self.valuebar.get_height()
        self.mana_valuebar = pygame.transform.scale(self.valuebar, (vb_w, int(vb_h * 0.5)))  #mana bar smaller by % 

        # values
        self.max_hp = 200
        self.hp = 200
        self.max_mana = 50
        self.mana = 50

        # --- TUNE ---
        self.valuebar_offset = pygame.Vector2(30, 9) * scale
        
        # ---- EXTRA FINETUNE OFFSETS (in pixels, worden ook gescaled) ----
        self.panel_offset      = pygame.Vector2(0, 0) * scale

        self.circle_nudge      = pygame.Vector2(-10, -4) * scale

        self.hp_bar_nudge      = pygame.Vector2(-8, 0) * scale
        self.mana_bar_nudge    = pygame.Vector2(-10, -0.4) * scale

        self.hp_fill_nudge     = pygame.Vector2(0, 0) * scale
        self.mana_fill_nudge   = pygame.Vector2(0, -2) * scale

        self.knots_nudge       = pygame.Vector2(0,0) * scale

        # ✅ spacing: gebaseerd op mana bar hoogte (netjes onder elkaar)
        self.valuebar_spacing = (vb_h - int(vb_h * 0.7)) + (10 * scale)  # klein gat
        # (als je wil tunen: zet gewoon bv 10*scale of 12*scale)

        self.fill_inset = pygame.Vector2(4, 4) * scale
        self.circle_offset = pygame.Vector2(-10, 0) * scale
        self.knot_inset = pygame.Vector2(0, 0) * scale

        # fill heights (ints!)
        self.red_height  = 8 * scale
        self.blue_height = 6.5 * scale

    def set_values(self, hp: int, mana: int, max_hp: int | None = None, max_mana: int | None = None):
        if max_hp is not None:
            self.max_hp = max(1, max_hp)
        if max_mana is not None:
            self.max_mana = max(1, max_mana)

        self.hp = max(0, min(hp, self.max_hp))
        self.mana = max(0, min(mana, self.max_mana))

    def _blit_fill(self, screen: pygame.Surface, img: pygame.Surface, topleft: tuple[int, int], ratio: float, height: int):
        ratio = max(0.0, min(1.0, ratio))
        w = int(img.get_width() * ratio)
        if w <= 0:
            return
        h = min(img.get_height(), int(height))
        part = img.subsurface(pygame.Rect(0, 0, w, h))
        screen.blit(part, topleft)

    def draw(self, screen: pygame.Surface):
        base = self.pos + self.panel_offset
        x, y = int(base.x), int(base.y)

        # panel
        screen.blit(self.panel, (x, y))
        pr = self.panel.get_rect(topleft=(x, y))

        # knots
        k = self.knot
        ki = self.knot_inset
        kn = self.knots_nudge
        screen.blit(k, (pr.right - k.get_width() + 5 - ki.x, pr.top + ki.y -5))     #top right
        screen.blit(k, (pr.right - k.get_width() - ki.x +5, pr.bottom - k.get_height() - ki.y +5))    #bottom right

        # positions
        vb1_pos = (x + int(self.valuebar_offset.x + self.hp_bar_nudge.x),
                y + int(self.valuebar_offset.y + self.hp_bar_nudge.y))

        vb2_pos = (vb1_pos[0] + int(self.mana_bar_nudge.x),
                vb1_pos[1] + int(self.valuebar_spacing) + int(self.mana_bar_nudge.y))

        hp_ratio = self.hp / self.max_hp
        mana_ratio = self.mana / self.max_mana

        hp_fill_pos = (vb1_pos[0] + int(self.fill_inset.x + self.hp_fill_nudge.x),
                    vb1_pos[1] + int(self.fill_inset.y + self.hp_fill_nudge.y))

        mana_fill_pos = (vb2_pos[0] + int(self.fill_inset.x + self.mana_fill_nudge.x),
                        vb2_pos[1] + int(self.fill_inset.y + self.mana_fill_nudge.y))
        
        # ✅ draw fill FIRST, then container (frame masks it nicely)
        self._blit_fill(screen, self.red,  hp_fill_pos,   hp_ratio,   self.red_height)
        screen.blit(self.valuebar, vb1_pos)

        self._blit_fill(screen, self.blue, mana_fill_pos, mana_ratio, self.blue_height)
        screen.blit(self.mana_valuebar, vb2_pos)
        
        # circle
        cpos = (x + int(self.circle_offset.x + self.circle_nudge.x),
            y + int(self.circle_offset.y + self.circle_nudge.y))
        screen.blit(self.circle, cpos)