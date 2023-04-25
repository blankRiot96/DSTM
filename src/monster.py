import pygame

from src.entity import Entity


class Monster(Entity):
    IMAGE = pygame.image.load("assets/monster.png").convert_alpha()
    ORIGINAL_SPEED = 75.0 + (15 * 6)
    SPEED = ORIGINAL_SPEED

    def __init__(self) -> None:
        super().__init__(self.IMAGE, self.SPEED)
        self.type_ = "monster"
