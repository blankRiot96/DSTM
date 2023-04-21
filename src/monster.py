import pygame

from src.entity import Entity


class Monster(Entity):
    IMAGE = pygame.image.load("assets/monster.png").convert_alpha()
    SPEED = 75.0

    def __init__(self) -> None:
        super().__init__(self.IMAGE, self.SPEED)
