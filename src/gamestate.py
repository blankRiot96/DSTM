import pygame

from src.citizen import Citizen
from src.monster import Monster
from src.shared import Shared
from src.state_enums import State
from src.utils import render_at


class GameState:
    def __init__(self) -> None:
        self.next_state: None | State = None
        self.shared = Shared()
        self.game_surface = pygame.Surface(
            ((80 / 100) * Shared.SCREEN_WIDTH, Shared.SCREEN_HEIGHT)
        )
        self.shared.game_surface = self.game_surface
        self.shared.grect = self.shared.game_surface.get_rect()

        self.shared.citizens: list[Citizen] = [Citizen() for _ in range(10)]
        # self.shared.monsters = []
        self.shared.monsters: list[Monster] = [Monster() for _ in range(20)]

    def update(self):
        for citizen in self.shared.citizens:
            citizen.update()
        for monster in self.shared.monsters:
            monster.update()

    def draw(self):
        # self.shared.screen.fill("black")
        self.game_surface.fill("seagreen")
        for citizen in self.shared.citizens:
            citizen.draw()
        for monster in self.shared.monsters:
            monster.draw()
        render_at(self.shared.screen, self.game_surface, "midright")
