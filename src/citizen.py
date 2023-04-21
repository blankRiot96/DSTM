import random
from enum import StrEnum, auto

import pygame

from src.entity import Entity


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
    SPEED = 50.0

    def __init__(self) -> None:
        self.type_ = random.choice(tuple(CitizenType))
        super().__init__(self.IMAGES[self.type_], self.SPEED)
