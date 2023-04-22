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
    MAX_BLINKS = 6
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

    def update(self):
        if self.rect.collidepoint(self.shared.mouse_pos):
            self.surf = self.hover_surf
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

    def alpha_adjust(self):
        self.overlay.set_alpha(self.alpha)
        if self.alpha >= 150.0:
            self.alpha = 150.0
            return
        self.alpha += 100.0 * self.shared.dt

    def update(self):
        self.alpha_adjust()
        self.gota.update()
        self.cta.update()
        self.main_menu_btn.update()
        self.retry_btn.update()

    def draw(self):
        self.shared.screen.blit(self.shared.last_frame, (0, 0))
        self.shared.screen.blit(self.overlay, (0, 0))
        self.gota.draw()
        self.cta.draw()
        self.main_menu_btn.draw()
        self.retry_btn.draw()
