import time

import pygame

from src.shared import Shared
from src.state_enums import State
from src.utils import Time, get_font, render_at


class GameOverTextAnimation:
    """Typing effect for 'GAME OVER' text"""

    FONT = get_font("assets/fonts/bold1.ttf", 64)
    TEXT_COLOR = (193, 184, 163)

    def __init__(self) -> None:
        self.shared = Shared()
        self.text = ""
        self.eventual_text = list(reversed("GAME OVER"))
        self.surf = self.FONT.render(self.text, True, self.TEXT_COLOR)
        self.timer = Time(0.3)

    def update(self):
        if self.timer.tick() and self.eventual_text:
            self.text += self.eventual_text.pop()
        self.surf = self.FONT.render(self.text, True, self.TEXT_COLOR)

    def draw(self):
        render_at(self.shared.screen, self.surf, "center", (0, -100))


class CauseTextAnimation:
    """Blinking effect for cause of death"""

    FONT = get_font("assets/fonts/bold1.ttf", 32)
    MAX_BLINKS = 6  # Not sure if I want a max blinks, will keep as dead code for now
    TEXT_COLOR = (193, 184, 163)

    def __init__(self) -> None:
        self.shared = Shared()
        self.surf = self.FONT.render(self.shared.lost_cause, True, self.TEXT_COLOR)
        self.timer = Time(0.5)
        self.show = True
        self.blinks = 0

    def update(self):
        # if self.blinks >= self.MAX_BLINKS:
        #     self.show = True
        #     return

        if self.timer.tick():
            self.show = not self.show
            self.blinks += 1

    def draw(self):
        if not self.show:
            return

        render_at(self.shared.screen, self.surf, "center")


class ScoreAnimation:
    """Running Score effect for below text

    FINAL SCORE
    lim 0 -> 312,000,231

    (yes with commas)
    """

    FONT = get_font("assets/fonts/bold1.ttf", 44)
    ANIM_SEC = 2.5
    TEXT_COLOR = (255, 255, 163)

    def __init__(self) -> None:
        self.shared = Shared()
        self.running_score = 0
        self.start = time.perf_counter()

    def update(self):
        if self.running_score >= self.shared.score:
            self.running_score = self.shared.score
            return

        time_passed = time.perf_counter() - self.start

        ratio = time_passed / self.ANIM_SEC
        self.running_score = self.shared.score * ratio
        self.running_score = int(self.running_score)

    def draw(self):
        surf = self.FONT.render(
            f"< {format(self.running_score, ',')} >", True, self.TEXT_COLOR
        )
        render_at(self.shared.screen, surf, "midtop", (0, 40))


class Button:
    FONT = get_font("assets/fonts/bold1.ttf", 24)
    TEXT_COLOR = (193, 184, 163)
    BACKGROUND_COLOR = (9, 24, 22)
    HOVER_COLOR = (23, 62, 61)

    def __init__(
        self, text: str, center: pygame.Vector2, size: tuple[int, int]
    ) -> None:
        self.shared = Shared()
        self.text = text
        self.center = center.copy()
        self.base_surf = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(
            self.base_surf,
            self.BACKGROUND_COLOR,
            (0, 0, *size),
            border_top_right_radius=10,
            border_bottom_left_radius=10,
        )

        self.hover_surf = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(
            self.hover_surf,
            self.HOVER_COLOR,
            (0, 0, *size),
            border_top_right_radius=10,
            border_bottom_left_radius=10,
        )

        self.outline_surf = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(
            self.outline_surf,
            "black",
            (0, 0, *size),
            border_top_right_radius=10,
            border_bottom_left_radius=10,
            width=3,
        )

        self.rect = self.base_surf.get_rect(center=self.center)

        self.surf = self.base_surf
        self.text_surf = self.FONT.render(self.text, True, self.TEXT_COLOR)
        self.text_rect = self.text_surf.get_rect(center=self.center)
        self.clicked = False

    def update(self):
        self.clicked = False

        clicked = False
        for event in self.shared.events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True

        if self.rect.collidepoint(self.shared.mouse_pos):
            self.surf = self.hover_surf
            if clicked:
                self.clicked = True
        else:
            self.surf = self.base_surf

    def draw(self):
        self.shared.screen.blit(self.surf, self.rect)
        self.shared.screen.blit(self.outline_surf, self.rect)
        self.shared.screen.blit(self.text_surf, self.text_rect)


class GameOver:
    def __init__(self) -> None:
        self.next_state: State | None = None
        self.shared = Shared()
        self.overlay = pygame.Surface(Shared.SRECT.size)
        self.overlay.fill((150, 0, 0))
        self.alpha = 0.0
        self.gota = GameOverTextAnimation()
        self.cta = CauseTextAnimation()

        self.main_menu_btn = Button(
            "main menu", self.shared.SRECT.center + pygame.Vector2(-100, 100), (150, 50)
        )
        self.retry_btn = Button(
            "retry", self.shared.SRECT.center + pygame.Vector2(100, 100), (150, 50)
        )

        self.running_score = ScoreAnimation()

    def alpha_adjust(self):
        self.overlay.set_alpha(self.alpha)
        if self.alpha >= 150.0:
            self.alpha = 150.0
            return
        self.alpha += 100.0 * self.shared.dt

    def update_menu_btn(self):
        self.main_menu_btn.update()

        if self.main_menu_btn.clicked:
            self.next_state = State.MENU

    def update_retry_btn(self):
        self.retry_btn.update()

        if self.retry_btn.clicked:
            self.next_state = State.GAME

    def update(self):
        self.alpha_adjust()
        self.gota.update()
        self.cta.update()
        self.update_menu_btn()
        self.update_retry_btn()
        self.running_score.update()

    def draw(self):
        self.shared.screen.blit(self.shared.last_frame, (0, 0))
        self.shared.screen.blit(self.overlay, (0, 0))
        self.gota.draw()
        self.cta.draw()
        self.main_menu_btn.draw()
        self.retry_btn.draw()
        self.running_score.draw()
