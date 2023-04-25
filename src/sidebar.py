import itertools
import random

import pygame

from src.citizen import Citizen, CitizenType
from src.king import King
from src.shared import Shared
from src.utils import Time, get_font, render_at


class SideBar:
    FONT_1 = get_font("assets/fonts/bold1.ttf", 32)
    FONT_2 = get_font("assets/fonts/bold1.ttf", 21)

    def __init__(self) -> None:
        self.shared = Shared()
        self.text_surf = self.FONT_2.render("TARGET", True, "BLACK")
        self.reset()

        self.score_surf = self.FONT_2.render(
            f"SCORE: {self.shared.score}", True, "black"
        )
        self.colors = itertools.cycle(("green", "black"))
        self.color = "black"
        self.timer = Time(0.5)
        self.once = True

    def gen_target_surf(self, image=None):
        if image is None:
            image = Citizen.IMAGES[self.target]
        self.target_surf = pygame.Surface((100, 120), pygame.SRCALPHA)
        pygame.draw.rect(
            self.target_surf, "black", (0, 0, *self.target_surf.get_size()), 5
        )
        render_at(self.target_surf, self.text_surf, "midtop", (0, 10))
        render_at(self.target_surf, image, "midbottom", (0, -15))

    def reset(self):
        if self.shared.winning:
            self.gen_target_surf(King.IMAGE)
            return
        self.target = random.choice(tuple(CitizenType))
        self.gen_target_surf()

    def update(self):
        if self.shared.winning:
            if self.timer.tick():
                self.color = next(self.colors)
        else:
            self.color = "black"

        self.score_surf = self.FONT_1.render(
            f"SCORE: {format(self.shared.score, ',')}", True, self.color
        )

    def draw(self):
        self.shared.screen.blit(self.score_surf, (10, 10))
        self.shared.screen.blit(self.target_surf, (50, 60))
        # render_at(self.shared.screen, self.target_surf, "midleft", ())
