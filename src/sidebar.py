import random

import pygame

from src.citizen import Citizen, CitizenType
from src.shared import Shared
from src.utils import get_font, render_at


class SideBar:
    FONT_1 = get_font("assets/fonts/bold2.ttf", 21)
    FONT_2 = get_font("assets/fonts/bold1.ttf", 21)

    def __init__(self) -> None:
        self.shared = Shared()
        self.text_surf = self.FONT_1.render("TARGET:", True, "black")
        self.reset()

        self.score_surf = self.FONT_2.render(
            f"SCORE: {self.shared.score}", True, "black"
        )

    def gen_target_surf(self):
        self.target_surf = pygame.Surface((100, 150), pygame.SRCALPHA)
        pygame.draw.rect(self.target_surf, "black", (0, 0, 100, 150), 10)
        render_at(self.target_surf, self.text_surf, "midtop", (0, 30))
        render_at(self.target_surf, Citizen.IMAGES[self.target], "midbottom", (0, -30))

    def reset(self):
        self.target = random.choice(tuple(CitizenType))
        self.gen_target_surf()

    def update(self):
        self.score_surf = self.FONT_2.render(
            f"SCORE: {format(self.shared.score, ',')}", True, "black"
        )

    def draw(self):
        self.shared.screen.blit(self.score_surf, (10, 10))
        self.shared.screen.blit(self.target_surf, (10, 60))
