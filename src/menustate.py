import pygame

from src.shared import Shared
from src.state_enums import State
from src.utils import SinWave, Time, get_font, render_at


class ClickAnywhere:
    """Typing effect for 'Click Anywhere' text"""

    FONT = get_font("assets/fonts/regular.ttf", 32)
    TEXT_COLOR = (193, 184, 163)

    def __init__(self) -> None:
        self.shared = Shared()
        self.text = ""
        self.eventual_text = list(reversed("< Click Anywhere To Begin >"))
        self.surf = self.FONT.render(self.text, True, self.TEXT_COLOR)
        self.timer = Time(0.15)

    def update(self):
        if self.timer.tick() and self.eventual_text:
            self.text += self.eventual_text.pop()
        self.surf = self.FONT.render(self.text, True, self.TEXT_COLOR)

    def draw(self):
        render_at(self.shared.screen, self.surf, "center", (0, 100))


class Banner:
    def __init__(self) -> None:
        self.shared = Shared()
        self.image = pygame.image.load("assets/banner.png").convert_alpha()
        self.wave = SinWave(0.005)
        self.y_offset = 0.0

    def update(self):
        self.y_offset = self.wave.val() * 15

    def draw(self):
        render_at(self.shared.screen, self.image, "center", (0, -100 + self.y_offset))


class MenuState:
    def __init__(self) -> None:
        self.shared = Shared()
        img = pygame.image.load("assets/cursor.png")
        # img = scale_by(img, 0.5)
        cursor = pygame.cursors.Cursor((0, 0), img)
        pygame.mouse.set_cursor(cursor)
        self.next_state: None | State = None
        self.bg_image = pygame.image.load("assets/background.png").convert()
        self.banner = Banner()
        self.click_anywhere = ClickAnywhere()

    def update(self):
        self.banner.update()
        self.click_anywhere.update()

        for event in self.shared.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.next_state = State.GAME

    def draw(self):
        self.shared.screen.blit(self.bg_image, (0, 0))
        self.banner.draw()
        self.click_anywhere.draw()
