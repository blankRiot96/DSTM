import random

import pygame

from src.entity import Entity
from src.utils import Time, scale_by


class King(Entity):
    IMAGE = pygame.image.load("assets/king.png").convert_alpha()
    IMAGE = scale_by(IMAGE, 0.5)
    ORIGINAL_SPEED = 200.0
    SPEED = ORIGINAL_SPEED

    def __init__(self) -> None:
        super().__init__(self.IMAGE, self.SPEED)
        self.type_ = "king"
        self.target = random.choice(self.shared.monsters).pos
        self.timer = Time(2.5)

    def move(self):
        self.pos.move_towards_ip(self.target, self.SPEED * self.shared.dt)
        self.rect.center = self.pos

    def update(self):
        super().update()
        if self.timer.tick():
            self.target = random.choice(self.shared.monsters).pos

    def draw(self):
        super().draw()
