import abc
import math
import random

import pygame

from src.shared import Shared


class Entity(abc.ABC):
    SPLAT_IMAGE = pygame.image.load("assets/splatter.png").convert_alpha()
    SPLAT_IMAGE.set_alpha(150)
    type_: str | object

    def __init__(self, image: pygame.Surface, speed: float) -> None:
        super().__init__()
        self.shared = Shared()
        self.image = image
        self.rect = self.image.get_rect()
        self.pos = pygame.Vector2(
            random.randint(
                self.rect.width, self.shared.game_surface.get_width() - self.rect.width
            ),
            random.randint(
                self.rect.height,
                self.shared.game_surface.get_height() - self.rect.height,
            ),
        )
        self.rect.center = self.pos
        self.direction = random.uniform(0.0, 2 * math.pi)
        self.direction_factor = 1
        self.speed = speed
        self.dx = math.cos(self.direction) * self.speed
        self.dy = math.sin(self.direction) * self.speed
        self.alive = True

    def move(self):
        dx = self.dx * self.shared.dt * self.direction_factor
        dy = self.dy * self.shared.dt * self.direction_factor

        self.pos += dx, dy
        self.rect.center = self.pos

    def bound(self):
        dx = self.dx * self.shared.dt * self.direction_factor
        dy = self.dy * self.shared.dt * self.direction_factor

        if not self.shared.grect.contains(self.rect.move(dx, dy)):
            self.direction_factor *= -1

    def on_death(self):
        if (
            self.rect.collidepoint(self.shared.target.gs_pos)
            and self.shared.target.clicked
        ):
            self.alive = False
            self.shared.target.score(self.type_)

    def update(self):
        if not self.alive:
            return
        self.bound()
        self.move()
        self.on_death()

    def draw_base(self):
        self.shared.game_surface.blit(self.image, self.rect)
        # pygame.draw.rect(self.shared.screen, "red", self.rect, 3)

    def draw_splatter(self):
        self.shared.game_surface.blit(self.SPLAT_IMAGE, self.rect)

    def draw(self):
        if not self.alive:
            self.draw_splatter()
            return
        self.draw_base()
