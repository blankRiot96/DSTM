import abc
import math
import random

import pygame

from src.shared import Shared


class Entity(abc.ABC):
    def __init__(self, image: pygame.Surface, speed: float) -> None:
        super().__init__()
        self.shared = Shared()
        self.image = image
        self.rect = self.image.get_rect()
        self.pos = pygame.Vector2(
            random.randint(0, self.shared.game_surface.get_width()),
            random.randint(0, self.shared.game_surface.get_height()),
        )
        self.rect.center = self.pos
        self.direction = random.uniform(0.0, 2 * math.pi)
        self.direction_factor = 1
        self.speed = speed

    def move(self):
        dx = (
            math.cos(self.direction)
            * self.speed
            * self.shared.dt
            * self.direction_factor
        )
        dy = (
            math.sin(self.direction)
            * self.speed
            * self.shared.dt
            * self.direction_factor
        )

        self.pos += dx, dy
        self.rect.center = self.pos

    def bound(self):
        if not self.shared.grect.contains(self.rect):
            self.direction_factor *= -1

    def update(self):
        self.move()
        self.bound()

    def draw_base(self):
        self.shared.game_surface.blit(self.image, self.rect)
        # pygame.draw.rect(self.shared.screen, "red", self.rect, 3)

    def draw(self):
        self.draw_base()
