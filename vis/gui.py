import os
import threading
import pygame

from src.MapLoader import MapLoader
from src.solver_factory import create_solver
from vis.simulator import SokobanSimulator, State

# ---------- UI CONSTANTS ----------
WIN_W, WIN_H = 1000, 700
LEFT_W = 280
BOTTOM_H = 90
MARGIN = 16

TILE = 40

COL_BG = (24, 24, 28)
COL_PANEL = (18, 18, 22)
COL_PANEL_BORDER = (60, 60, 70)
COL_TEXT = (235, 235, 235)
COL_MUTED = (170, 170, 170)

COL_WALL = (90, 90, 95)
COL_FLOOR = (40, 40, 46)
COL_GRID = (55, 55, 62)

COL_GOAL = (220, 190, 70)
COL_BOX = (170, 120, 70)
COL_BOX_GOAL = (80, 190, 130)
COL_PLAYER = (90, 155, 250)

COL_BTN = (60, 90, 160)
COL_BTN_HOVER = (80, 115, 200)
COL_BTN_DISABLED = (70, 70, 80)

FPS = 60
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------- Helpers ----------
def list_map_files(maps_dir):
    if not os.path.isdir(maps_dir):
        return []
    files = [f for f in os.listdir(maps_dir) if f.lower().endswith(".txt")]
    files.sort()
    return [os.path.join(maps_dir, f) for f in files]


class Button:
    def __init__(self, rect, text, on_click):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.on_click = on_click
        self.enabled = True

    def draw(self, surf, font, mouse_pos):
        hovering = self.rect.collidepoint(mouse_pos)
        if not self.enabled:
            col = COL_BTN_DISABLED
        else:
            col = COL_BTN_HOVER if hovering else COL_BTN

        pygame.draw.rect(surf, col, self.rect, border_radius=10)
        pygame.draw.rect(surf, (0,0,0), self.rect, 2, border_radius=10)

        label = font.render(self.text, True, (255,255,255))
        surf.blit(label, label.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if not self.enabled:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.on_click()

class MapList:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.items = []  # list[str] full paths
        self.selected_idx = -1
        self.scroll = 0
        self.row_h = 34

    def set_items(self, items):
        self.items = items
        self.selected_idx = -1
        self.scroll = 0

    def selected_path(self):
        if 0 <= self.selected_idx < len(self.items):
            return self.items[self.selected_idx]
        return None

    def draw(self, surf, font, small_font, mouse_pos):
        # panel
        pygame.draw.rect(surf, COL_PANEL, self.rect, border_radius=12)
        pygame.draw.rect(surf, COL_PANEL_BORDER, self.rect, 2, border_radius=12)

        title = font.render("Maps", True, COL_TEXT)
        surf.blit(title, (self.rect.x + 12, self.rect.y + 10))

        inner = pygame.Rect(self.rect.x + 8, self.rect.y + 44, self.rect.w - 16, self.rect.h - 52)
        pygame.draw.rect(surf, (14,14,18), inner, border_radius=10)

        # clipping
        clip_prev = surf.get_clip()
        surf.set_clip(inner)

        start_y = inner.y - self.scroll
        for i, path in enumerate(self.items):
            name = os.path.basename(path)
            row = pygame.Rect(inner.x, start_y + i*self.row_h, inner.w, self.row_h)

            is_sel = (i == self.selected_idx)
            is_hover = row.collidepoint(mouse_pos)

            if is_sel:
                pygame.draw.rect(surf, (50, 70, 120), row, border_radius=6)
            elif is_hover:
                pygame.draw.rect(surf, (35, 35, 45), row, border_radius=6)

            label = small_font.render(name, True, COL_TEXT if (is_sel or is_hover) else COL_MUTED)
            surf.blit(label, (row.x + 10, row.y + 8))

        surf.set_clip(clip_prev)

        # scrollbar hint
        hint = small_font.render("Scroll: mouse wheel", True, COL_MUTED)
        surf.blit(hint, (self.rect.x + 12, self.rect.bottom - 26))

    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            # wheel works everywhere; if you want only when hover: check pos
            self.scroll -= event.y * 30
            self.scroll = max(0, self.scroll)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not self.rect.collidepoint(event.pos):
                return
            # click inside list
            inner = pygame.Rect(self.rect.x + 8, self.rect.y + 44, self.rect.w - 16, self.rect.h - 52)
            if not inner.collidepoint(event.pos):
                return
            local_y = event.pos[1] - inner.y + self.scroll
            idx = local_y // self.row_h
            if 0 <= idx < len(self.items):
                self.selected_idx = int(idx)

# ---------- Main App ----------
class SokobanGUI:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sokoban SAT Solver - GUI")
        self.screen = pygame.display.set_mode((WIN_W, WIN_H), pygame.RESIZABLE)

        self.sprites = self.load_sprites()
        self.sprite_cache = {}  # cache scaled sprites (speed)

        self.font = pygame.font.SysFont("consolas", 22, bold=True)
        self.small = pygame.font.SysFont("consolas", 18)
        self.tiny = pygame.font.SysFont("consolas", 15)

        self.clock = pygame.time.Clock()

        self.maps = list_map_files(os.path.join(BASE_DIR, "maps"))

        # Layout rects (will be updated on resize)
        self.map_list = MapList((MARGIN, MARGIN, LEFT_W - 2*MARGIN, WIN_H - BOTTOM_H - 2*MARGIN))
        self.map_list.set_items(self.maps)

        self.solve_btn = Button((LEFT_W + 2*MARGIN, WIN_H - BOTTOM_H + 18, 220, 54), "Solve", self.on_solve_clicked)

        self.status = "Select a map"
        self.error = None

        # Map/game state
        self.map_path = None
        self.map_data = None
        self.sim = None
        self.init_state = None

        self.plan = []
        self.states = []
        self.step_idx = 0

        # animation
        self.playing = False
        self.step_delay_ms = 160
        self._last_tick = 0

        # solving thread
        self.solving = False

    def load_sprites(self):
        assets_dir = os.path.join(BASE_DIR, "vis", "assets")

        def load(name):
            img = pygame.image.load(os.path.join(assets_dir, name))
            if name.lower().endswith(".png"):
                return img.convert_alpha()
            return img.convert()

        return {
            "wall": load("wall.jpg"),
            "floor": load("floor.jpg"),
            "goal": load("goal.png"),
            "box": load("box.png"),
            "box_goal": load("box_goal.png"),
            "player": load("sokoban.png"),
        }

    def draw_sprite(self, key, x, y, size):
        cache_key = (key, size)
        img = self.sprite_cache.get(cache_key)
        if img is None:
            img = pygame.transform.smoothscale(self.sprites[key], (size, size))
            self.sprite_cache[cache_key] = img
        self.screen.blit(img, (x, y))

    def layout(self):
        w, h = self.screen.get_size()
        self.map_list.rect = pygame.Rect(MARGIN, MARGIN, LEFT_W - 2*MARGIN, h - BOTTOM_H - 2*MARGIN)
        self.solve_btn.rect = pygame.Rect(LEFT_W + 2*MARGIN, h - BOTTOM_H + 18, 220, 54)

    def load_selected_map(self):
        path = self.map_list.selected_path()
        if not path:
            return
        try:
            data = MapLoader().load_map(path)
            walls = set(data["walls"])
            goals = set(data["goals"])
            player = data["sokoban"]
            boxes = frozenset(data["boxes"])

            self.map_path = path
            self.map_data = data
            self.sim = SokobanSimulator(walls, goals)
            self.init_state = State(player=player, boxes=boxes)

            self.plan = []
            self.states = [self.init_state]
            self.step_idx = 0
            self.playing = False

            self.status = f"Loaded: {os.path.basename(path)}"
            self.error = None
        except Exception as e:
            self.error = str(e)
            self.status = "Failed to load map"

    def on_solve_clicked(self):
        if self.solving or not self.map_path:
            return

        self.solving = True
        self.playing = False
        self.error = None
        self.status = "Solving with Minisat..."

        def worker():
            try:
                ss = create_solver(self.map_path, limit=80)
                plan = ss.solve_and_return_plan()

                if not plan:
                    self.plan = []
                    self.states = [self.init_state]
                    self.step_idx = 0
                    self.status = "No solution (or limit reached)"
                    return

                # build states
                st = [self.init_state]
                for a in plan:
                    st.append(self.sim.step(st[-1], a))
                self.plan = plan
                self.states = st
                self.step_idx = 0

                self.status = f"Solved! Plan length: {len(plan)}. Playing..."
                self.playing = True
                self._last_tick = pygame.time.get_ticks()

            except Exception as e:
                self.error = str(e)
                self.status = "Solve failed"
            finally:
                self.solving = False

        threading.Thread(target=worker, daemon=True).start()

    def tick_autoplay(self):
        if not self.playing:
            return
        now = pygame.time.get_ticks()
        if now - self._last_tick >= self.step_delay_ms:
            self._last_tick = now
            if self.step_idx < len(self.states) - 1:
                self.step_idx += 1
            else:
                self.playing = False
                # optionally show goal status
                if self.sim and self.sim.is_goal(self.states[-1]):
                    self.status = "Finished"
                else:
                    self.status = "Playback ended"

    def compute_tile_size(self):
        # Fit board into available area (right side, above bottom bar)
        if not self.map_data:
            return TILE
        w, h = self.screen.get_size()
        avail_w = w - LEFT_W - 3*MARGIN
        avail_h = h - BOTTOM_H - 2*MARGIN

        rows, cols = self.map_data["map_size"]
        if rows <= 0 or cols <= 0:
            return TILE

        tile_w = max(16, avail_w // cols)
        tile_h = max(16, avail_h // rows)
        return min(tile_w, tile_h, 64)

    def draw_board(self):
        if not self.map_data:
            return

        w, h = self.screen.get_size()
        tile = self.compute_tile_size()

        rows, cols = self.map_data["map_size"]
        board_w = cols * tile
        board_h = rows * tile

        origin_x = LEFT_W + 2*MARGIN
        origin_y = MARGIN + 10

        # background for board area
        board_rect = pygame.Rect(origin_x - 10, origin_y - 10, board_w + 20, board_h + 20)
        pygame.draw.rect(self.screen, (16,16,20), board_rect, border_radius=14)
        pygame.draw.rect(self.screen, COL_PANEL_BORDER, board_rect, 2, border_radius=14)

        walls = set(self.map_data["walls"])
        goals = set(self.map_data["goals"])
        state = self.states[self.step_idx] if self.states else self.init_state
        boxes = set(state.boxes)
        px, py = state.player

        # floor
        pygame.draw.rect(self.screen, COL_FLOOR, (origin_x, origin_y, board_w, board_h))

        for r in range(rows):
            for c in range(cols):
                cell = (r, c)
                x = origin_x + c * tile
                y = origin_y + r * tile
                cell_rect = pygame.Rect(x, y, tile, tile)

                # floor always
                self.draw_sprite("floor", x, y, tile)

                if cell in walls:
                    self.draw_sprite("wall", x, y, tile)
                else:
                    if cell in goals:
                        self.draw_sprite("goal", x, y, tile)

                    if cell in boxes:
                        self.draw_sprite("box_goal" if cell in goals else "box", x, y, tile)

                    if cell == (px, py):
                        self.draw_sprite("player", x, y, tile)

                pygame.draw.rect(self.screen, COL_GRID, cell_rect, 1)  # optional grid

        # overlay: step/action
        action_txt = "-"
        if self.plan and self.step_idx > 0:
            action_txt = self.plan[self.step_idx - 1]

        info = f"Step {self.step_idx}/{max(0, len(self.states)-1)}"
        label = self.small.render(info, True, COL_TEXT)
        self.screen.blit(label, (origin_x, origin_y + board_h + 14))

    def draw_bottom_bar(self):
        w, h = self.screen.get_size()
        bar = pygame.Rect(LEFT_W, h - BOTTOM_H, w - LEFT_W, BOTTOM_H)
        pygame.draw.rect(self.screen, COL_PANEL, bar)
        pygame.draw.rect(self.screen, COL_PANEL_BORDER, bar, 2)

        # status text
        status_col = (255, 200, 90) if self.solving else COL_TEXT
        st = self.small.render(self.status, True, status_col)
        self.screen.blit(st, (LEFT_W + 2*MARGIN + 260, h - BOTTOM_H + 18))

        if self.error:
            err = self.tiny.render(self.error, True, (255, 120, 120))
            self.screen.blit(err, (LEFT_W + 2*MARGIN + 260, h - BOTTOM_H + 48))

    def update_buttons(self):
        # Solve enabled only if map loaded and not solving
        self.solve_btn.enabled = (self.map_path is not None and not self.solving)

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            self.layout()
            self.update_buttons()

            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                # map list events
                self.map_list.handle_event(event)

                # on click selection => load map
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # if clicked inside map list and selected changed, load
                    before = self.map_path
                    self.load_selected_map()

                # solve button
                self.solve_btn.handle_event(event)

            # autoplay
            self.tick_autoplay()

            # draw
            self.screen.fill(COL_BG)
            self.map_list.draw(self.screen, self.font, self.small, mouse_pos)
            self.draw_board()
            self.draw_bottom_bar()

            # button (bottom)
            self.solve_btn.draw(self.screen, self.small, mouse_pos)

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    SokobanGUI().run()
