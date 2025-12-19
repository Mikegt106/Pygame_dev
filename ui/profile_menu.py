# ui/profile_menu.py
import pygame


class ProfileMenu:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.visible = False

        # SFX
        self.hover_sfx = pygame.mixer.Sound("assets/Sounds/hover.wav")
        self.hover_sfx.set_volume(0.5)
        self._last_hover = None

        # fonts
        self.title_font = pygame.font.SysFont(None, 72)
        self.text_font  = pygame.font.SysFont(None, 28)
        self.small_font = pygame.font.SysFont(None, 26)

        # panel
        sw, sh = self.screen.get_size()
        self.panel_w = int(sw * 0.68)
        self.panel_h = int(sh * 0.62)
        self.panel = pygame.Surface((self.panel_w, self.panel_h), pygame.SRCALPHA)
        self.panel_rect = self.panel.get_rect(center=(sw // 2, sh // 2))

        # button assets (raw)
        self.btn_raw = pygame.image.load("assets/Buttons/Button.png").convert_alpha()
        self.hl_raw  = pygame.image.load("assets/Buttons/Highlight.png").convert_alpha()

        # autosize padding
        self.pad_x = 30
        self.pad_y = 5
        self.max_btn_h = 45  # hoe “dun” de knop is

        # highlight padding
        self.hl_pad_x = 10
        self.hl_pad_y = 6

        # caches: (w,h)->Surface
        self._btn_cache = {}
        self._hl_cache = {}

        # rects (worden gezet in _layout)
        self.upg_hp_rect = pygame.Rect(0, 0, 0, 0)
        self.upg_mana_rect = pygame.Rect(0, 0, 0, 0)
        self.upg_dmg_rect = pygame.Rect(0, 0, 0, 0)
        self.close_rect = pygame.Rect(0, 0, 0, 0)

    def toggle(self):
        self.visible = not self.visible
        if not self.visible:
            self._last_hover = None

    # -------------------------
    # helpers
    # -------------------------
    def _get_scaled_btn(self, w, h):
        key = (int(w), int(h))
        if key not in self._btn_cache:
            self._btn_cache[key] = pygame.transform.scale(self.btn_raw, key)
        return self._btn_cache[key]

    def _get_scaled_hl(self, w, h):
        key = (int(w), int(h))
        if key not in self._hl_cache:
            self._hl_cache[key] = pygame.transform.scale(self.hl_raw, key)
        return self._hl_cache[key]

    def _autosize_single_line(self, text: str):
        surf = self.text_font.render(text, True, (0, 0, 0))
        w = surf.get_width() + self.pad_x * 2
        h = surf.get_height() + self.pad_y * 2
        h = min(h, self.max_btn_h)  # dun houden
        return int(w), int(h)

    def _layout(self, player, config):
        # stats layout
        left_x = self.panel_rect.x + 50
        base_y = self.panel_rect.y + 120
        line_step = 40

        hp_y   = base_y + 0 * line_step
        mana_y = base_y + 1 * line_step
        dmg_y  = base_y + 2 * line_step

        # costs
        hp_cost, mana_cost, dmg_cost = player.upgrade_costs()

        # ✅ 1 lijn: "UPGRADE  40c" (langs elkaar)
        hp_text   = f"UPG   {hp_cost}coins"
        mana_text = f"UPG   {mana_cost}coins"
        dmg_text  = f"UPG   {dmg_cost}coins"

        # autosize per knop (breedte volgt tekst)
        hp_w, hp_h     = self._autosize_single_line(hp_text)
        mana_w, mana_h = self._autosize_single_line(mana_text)
        dmg_w, dmg_h   = self._autosize_single_line(dmg_text)

        # kolom rechts in panel
        right_margin = 400
        col_x = self.panel_rect.right - right_margin

        def place_for_y(btn_w, btn_h, stat_y):
            x = col_x - btn_w
            y = stat_y - (btn_h // 2) + 10
            return pygame.Rect(x, y, btn_w, btn_h)

        self.upg_hp_rect   = place_for_y(hp_w, hp_h, hp_y)
        self.upg_mana_rect = place_for_y(mana_w, mana_h, mana_y)
        self.upg_dmg_rect  = place_for_y(dmg_w, dmg_h, dmg_y)

        # close knop (autosize)
        close_text = "CLOSE"
        close_w, close_h = self._autosize_single_line(close_text)
        bx = self.panel_rect.centerx - close_w // 2
        by = self.panel_rect.bottom - close_h - 28
        self.close_rect = pygame.Rect(bx, by, close_w, close_h)

        return (hp_cost, mana_cost, dmg_cost, hp_text, mana_text, dmg_text, close_text)

    def _hover_index(self, mx, my):
        if self.upg_hp_rect.collidepoint((mx, my)): return 0
        if self.upg_mana_rect.collidepoint((mx, my)): return 1
        if self.upg_dmg_rect.collidepoint((mx, my)): return 2
        if self.close_rect.collidepoint((mx, my)): return 3
        return None

    # -------------------------
    def handle_event(self, event, player, config):
        if not self.visible:
            return None

        # rects up-to-date houden
        self._layout(player, config)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.visible = False
            self._last_hover = None
            return "close"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.upg_hp_rect.collidepoint(event.pos):
                return "up_hp"
            if self.upg_mana_rect.collidepoint(event.pos):
                return "up_mana"
            if self.upg_dmg_rect.collidepoint(event.pos):
                return "up_dmg"
            if self.close_rect.collidepoint(event.pos):
                self.visible = False
                self._last_hover = None
                return "close"

        return None

    def draw(self, player, config):
        if not self.visible:
            return

        hp_cost, mana_cost, dmg_cost, hp_text, mana_text, dmg_text, close_text = self._layout(player, config)

        # overlay
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))

        # panel bg
        self.panel.fill((0, 0, 0, 0))
        pygame.draw.rect(self.panel, (30, 30, 30, 235), self.panel.get_rect(), border_radius=18)
        pygame.draw.rect(self.panel, (255, 255, 255, 70), self.panel.get_rect(), width=2, border_radius=18)
        self.screen.blit(self.panel, self.panel_rect.topleft)

        # title
        title = self.title_font.render("PROFILE", True, (255, 255, 255))
        self.screen.blit(title, (self.panel_rect.x + 40, self.panel_rect.y + 30))

        # stats
        hp = getattr(player, "hp", 0)
        max_hp = getattr(player, "max_hp", hp)
        mana = int(getattr(player, "mana", 0))
        max_mana = int(getattr(player, "max_mana", mana))
        coins = getattr(player, "coins", 0)

        base_dmg = int(getattr(config, "DAMAGE", {}).get("book", 1))
        dmg = base_dmg + getattr(player, "damage_bonus", 0)

        left_x = self.panel_rect.x + 50
        base_y = self.panel_rect.y + 120
        line_step = 40

        y = base_y
        for text in [
            f"HP: {hp} / {max_hp}",
            f"MANA: {mana} / {max_mana}",
            f"DAMAGE: {dmg}",
            f"COINS: {coins}",
        ]:
            t = self.text_font.render(text, True, (230, 230, 230))
            self.screen.blit(t, (left_x, y))
            y += line_step

        # hover detect + sound
        mx, my = pygame.mouse.get_pos()
        hovered_idx = self._hover_index(mx, my)
        if hovered_idx is not None and hovered_idx != self._last_hover:
            self.hover_sfx.play()
        self._last_hover = hovered_idx

        def draw_btn(rect: pygame.Rect, text: str, can_buy: bool, is_hovered: bool):
            btn = self._get_scaled_btn(rect.w, rect.h)
            hl  = self._get_scaled_hl(rect.w + self.hl_pad_x * 2, rect.h + self.hl_pad_y * 2)

            if is_hovered:
                self.screen.blit(hl, (rect.x - self.hl_pad_x, rect.y - self.hl_pad_y))
            self.screen.blit(btn, rect.topleft)

            # 1 lijn centreren
            txt = self.text_font.render(text, True, (25, 25, 25))
            tr = txt.get_rect(center=rect.center)
            self.screen.blit(txt, tr)

            # lock overlay
            if not can_buy:
                shade = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
                self.screen.blit(shade, rect.topleft)

        draw_btn(self.upg_hp_rect,   hp_text,   player.can_afford(hp_cost),   hovered_idx == 0)
        draw_btn(self.upg_mana_rect, mana_text, player.can_afford(mana_cost), hovered_idx == 1)
        draw_btn(self.upg_dmg_rect,  dmg_text,  player.can_afford(dmg_cost),  hovered_idx == 2)

        # close button
        close_btn = self._get_scaled_btn(self.close_rect.w, self.close_rect.h)
        close_hl  = self._get_scaled_hl(self.close_rect.w + self.hl_pad_x * 2, self.close_rect.h + self.hl_pad_y * 2)

        if hovered_idx == 3:
            self.screen.blit(close_hl, (self.close_rect.x - self.hl_pad_x, self.close_rect.y - self.hl_pad_y))
        self.screen.blit(close_btn, self.close_rect.topleft)

        txt = self.text_font.render(close_text, True, (25, 25, 25))
        tr = txt.get_rect(center=self.close_rect.center)
        self.screen.blit(txt, tr)