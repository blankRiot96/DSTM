import pygame

from src.citizen import Citizen
from src.monster import Monster
from src.shared import Shared
from src.sidebar import SideBar
from src.state_enums import State
from src.target import Target
from src.utils import Time, render_at


class GameState:
    def __init__(self) -> None:
        self.next_state: None | State = None
        self.shared = Shared(score=0, lost=False, lost_cause="")
        self.shared.total_time = 10
        self.shared.time_left = self.shared.total_time
        self.game_surface = pygame.Surface(
            ((80 / 100) * Shared.SCREEN_WIDTH, Shared.SCREEN_HEIGHT)
        )
        self.shared.game_surface = self.game_surface
        self.shared.grect = self.shared.game_surface.get_rect()

        self.shared.target = Target()

        self.shared.citizens: list[Citizen] = [Citizen() for _ in range(15)]
        # self.shared.monsters = []
        self.shared.monsters: list[Monster] = [Monster() for _ in range(15)]
        self.timer = Time(1.0)

        self.shared.sidebar = SideBar()

    def reset(self):
        if self.shared.total_time > 4:
            self.shared.total_time -= 2
        self.shared.time_left = self.shared.total_time

        self.shared.citizens: list[Citizen] = [Citizen() for _ in range(15)]
        # self.shared.monsters = []
        self.shared.monsters: list[Monster] = [Monster() for _ in range(15)]
        self.shared.sidebar.reset()

    def update(self):
        self.shared.target.update()
        for citizen in self.shared.citizens:
            citizen.update()
        for monster in self.shared.monsters:
            monster.update()

        if self.timer.tick():
            self.shared.target.reset_time_per_second()
            self.shared.time_left -= 1
            if self.shared.time_left < 0:
                self.reset()

        self.shared.sidebar.update()

        if self.shared.lost:
            pygame.mouse.set_cursor(self.shared.target.ui_cursor)
            self.next_state = State.GAME_OVER
            self.draw()
            self.shared.last_frame = self.shared.screen.copy()

    def draw(self):
        # self.shared.screen.fill("black")
        self.game_surface.fill("seagreen")
        for citizen in self.shared.citizens:
            citizen.draw()
        for monster in self.shared.monsters:
            monster.draw()
        self.shared.target.draw()
        render_at(self.shared.screen, self.game_surface, "midright")
        self.shared.sidebar.draw()
