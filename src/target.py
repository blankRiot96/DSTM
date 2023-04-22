import pygame

from src.shared import Shared
from src.utils import get_font, render_at, scale_by


class Target:
    SCORE_FONT = get_font("assets/fonts/bold1.ttf", 32)
    TIME_FONT = get_font("assets/fonts/bold1.ttf", 64)

    def __init__(self) -> None:
        self.shared = Shared()
        self.gs_pos = (0, 0)
        self.target_cursor = self.gen_target_cursor()
        self.ui_cursor = self.gen_ui_cursor()
        self.clicked = False
        self.max_score_gain = 100
        self.score_gain = self.max_score_gain
        self.score_surf = self.SCORE_FONT.render(str(self.score_gain), True, "white")
        self.time_left_surf = self.TIME_FONT.render(
            str(self.shared.time_left), True, "black"
        )
        self.time_size = 1

    def gen_target_cursor(self):
        img = pygame.image.load("assets/target.png")
        img = scale_by(img, 0.1)
        center = img.get_rect().center
        cursor = pygame.cursors.Cursor(center, img)
        return cursor
        # pygame.mouse.set_cursor(pygame.cursors.Cursor(center, img))

    def gen_ui_cursor(self):
        img = pygame.image.load("assets/cursor.png")
        # img = scale_by(img, 0.5)
        cursor = pygame.cursors.Cursor((0, 0), img)
        return cursor

    def gen_pos(self):
        self.gs_pos = self.shared.mouse_pos - pygame.Vector2(
            self.shared.SCREEN_WIDTH - self.shared.grect.width, 0
        )

    def toggle_cursor(self):
        # The mouse position is within the sidebar
        if (
            self.shared.mouse_pos[0]
            < self.shared.SCREEN_WIDTH - self.shared.grect.width
        ):
            pygame.mouse.set_cursor(self.ui_cursor)
        else:
            pygame.mouse.set_cursor(self.target_cursor)

    def on_click(self):
        self.clicked = False
        for event in self.shared.events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.clicked = True
                return

    def score(self, type_):
        if type_ == self.shared.sidebar.target:
            self.shared.score += self.score_gain
        elif type_ == "monster":
            print("YOU SHOT THE MONSTER")
        else:
            self.shared.score -= self.score_gain

        found = False
        for citizen in self.shared.citizens:
            if citizen.alive and citizen.type_ == self.shared.sidebar.target:
                found = True

        if not found:
            self.shared.time_left = 0

    def reset_time_per_second(self):
        self.time_size = 1

    def update(self):
        self.gen_pos()
        self.toggle_cursor()
        self.on_click()
        self.score_surf = self.SCORE_FONT.render(str(self.score_gain), True, "black")
        self.score_gain = self.max_score_gain * (
            self.shared.time_left / self.shared.total_time
        )
        self.score_gain = int(self.score_gain)
        if self.shared.time_left > 3:
            color = "black"
        else:
            color = (150, 0, 0)
        self.time_left_surf = self.TIME_FONT.render(
            str(self.shared.time_left), True, color
        )

        self.time_left_surf = scale_by(self.time_left_surf, self.time_size)
        self.time_size -= 0.5 * self.shared.dt

    def draw(self):
        render_at(self.shared.game_surface, self.score_surf, "topright")
        render_at(self.shared.game_surface, self.time_left_surf, "midtop")
