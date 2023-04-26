import random

import pygame

from src.shared import Shared
from src.utils import SinWave, scale_by


class StarMultiplier:
    """
    A Star Multiplier that grants 2x score boost
    for the round
    """

    ORIGINAL_IMAGE = pygame.image.load("assets/star.png").convert_alpha()
    ORIGINAL_IMAGE = scale_by(ORIGINAL_IMAGE, 1.5)
    SFX = pygame.mixer.Sound("assets/audio/star-sfx.wav")

    def __init__(self) -> None:
        self.shared = Shared()
        self.pos = (
            random.randrange(self.shared.grect.width - 100),
            random.randrange(self.shared.grect.height - 100),
        )
        self.image = self.ORIGINAL_IMAGE.copy()
        self.rect = self.image.get_rect(center=self.pos)
        self.angle = 0
        self.rotational_speed = 100.3
        self.original_size = self.rect.size[0]
        self.size_wave = SinWave(0.1)
        self.used = False

    def rotate(self):
        self.angle += self.rotational_speed * self.shared.dt
        if self.angle >= 359:
            self.angle = 0

        self.image = pygame.transform.rotate(self.ORIGINAL_IMAGE, self.angle)

    def wobble(self):
        size = self.original_size + ((self.size_wave.val() * 2) * self.shared.dt)

        self.image = pygame.transform.scale(self.image, (size, size))

    def update(self):
        self.rotate()
        self.wobble()
        self.rect = self.image.get_rect(center=self.pos)

        if (
            self.rect.collidepoint(self.shared.target.gs_pos)
            and self.shared.target.clicked
        ):
            self.shared.target.score_multiplier *= 2
            self.used = True
            self.SFX.play()

    def draw(self):
        self.shared.game_surface.blit(self.image, self.rect)


class StarManager:
    """Splatters stars around the screen"""

    def __init__(self) -> None:
        self.shared = Shared()
        self.stars: list[StarMultiplier] = []

    def reset(self):
        if self.shared.rounds < 3:
            return

        self.stars = [StarMultiplier() for _ in range(random.randrange(3))]
        self.shared.target.score_multiplier = 1

    def update(self):
        for star in self.stars[:]:
            star.update()

            if star.used:
                self.stars.remove(star)

    def draw(self):
        for star in self.stars:
            star.draw()
