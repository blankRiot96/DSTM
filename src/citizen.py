import random
from enum import StrEnum, auto

import pygame

from src.entity import Entity
from src.utils import get_font


class CitizenType(StrEnum):
    GREEN = auto()
    BLUE = auto()
    RED = auto()
    YELLOW = auto()


class Citizen(Entity):
    IMAGES = {
        T: pygame.image.load(f"assets/{T.value}.png").convert_alpha()
        for T in CitizenType
    }
    ORIGINAL_SPEED = 50.0
    FONT = get_font("assets/fonts/regular.ttf", 32)
    SPEED = ORIGINAL_SPEED

    def __init__(self, type_: CitizenType | None = None) -> None:
        if type_ is None:
            self.type_ = random.choice(tuple(CitizenType))
        else:
            self.type_ = type_
        super().__init__(self.IMAGES[self.type_], self.SPEED)
        self.vertical_diff = 0.0
        self.surf_speed = 150.0
        self.surf_alpha = 255.0
        self.alpha_reduction_speed = 400.0

    def on_death(self):
        super().on_death()

        if self.alive:
            return False

        if self.type_ == self.shared.sidebar.target:
            p = self.shared.target.score_gain * self.shared.target.score_multiplier
            color = "green"
            symbol = "+"
        else:
            p = self.shared.target.score_gain
            color = "red"
            symbol = "-"
        self.score_surf = self.FONT.render(f"{symbol}{p:.0f}", True, color)
        self.score_rect = self.score_surf.get_rect(center=self.rect.center)

    def update(self):
        super().update()
        if self.alive or self.surf_alpha <= 0.0:
            return

        self.vertical_diff -= self.surf_speed * self.shared.dt
        self.surf_alpha -= self.alpha_reduction_speed * self.shared.dt
        self.score_surf.set_alpha(self.surf_alpha)

    def draw(self):
        super().draw()
        if self.alive:
            return

        self.shared.game_surface.blit(
            self.score_surf, self.score_rect.move(0, self.vertical_diff)
        )
