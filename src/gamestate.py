import pygame

from src.citizen import Citizen, CitizenType
from src.king import King
from src.monster import Monster
from src.multiplier import StarManager
from src.shared import Shared
from src.sidebar import SideBar
from src.state_enums import State
from src.target import Target
from src.utils import Time, render_at


class GameState:
    def __init__(self) -> None:
        Citizen.SPEED = Citizen.ORIGINAL_SPEED
        Monster.SPEED = Monster.ORIGINAL_SPEED
        self.next_state: None | State = None
        self.shared = Shared(
            score=0,
            lost=False,
            lost_cause="",
            shot_target=False,
            rounds=0,
            winning=False,
            king=None,
            won=False,
        )
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

        self.star_manager = StarManager()
        self.star_manager.reset()
        self.not_first = False
        self.light = pygame.image.load("assets/light.png").convert()
        self.light_rect = self.light.get_rect()
        self.overlay = pygame.Surface(self.game_surface.get_size())

    def reset(self):
        self.shared.rounds += 1

        if self.shared.rounds < 10:
            Citizen.SPEED += 15
            Monster.SPEED += 15
        if not self.shared.shot_target:
            self.shared.lost = True
            self.shared.lost_cause = "You Didn't Shoot The Target!"

        if self.shared.total_time > 5:
            self.shared.total_time -= 1

        self.shared.time_left = self.shared.total_time

        # self.shared.monsters = []
        self.shared.sidebar.reset()

        self.shared.shot_target = False
        self.star_manager.reset()

        if self.shared.score >= Shared.WIN_SCORE:
            n_monsters = 50
            self.shared.monsters: list[Monster] = [Monster() for _ in range(n_monsters)]
            self.shared.citizens.clear()
            self.shared.total_time = 25
            self.shared.time_left = self.shared.total_time
            self.shared.king = King()
            return
        else:
            n_monsters = 15

        self.shared.monsters: list[Monster] = [Monster() for _ in range(n_monsters)]
        self.shared.citizens: list[Citizen] = [Citizen() for _ in range(11)]
        self.shared.citizens.extend(
            [
                Citizen(CitizenType.BLUE),
                Citizen(CitizenType.GREEN),
                Citizen(CitizenType.RED),
                Citizen(CitizenType.YELLOW),
            ]
        )

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
                if self.shared.winning and self.not_first:
                    self.shared.lost = True
                    self.not_first = True
                else:
                    self.reset()

        if self.shared.score >= Shared.WIN_SCORE:
            if not self.shared.winning:
                self.shared.time_left = 0
            self.shared.winning = True

        self.shared.sidebar.update()
        self.star_manager.update()

        if self.shared.lost:
            pygame.mouse.set_cursor(self.shared.target.ui_cursor)
            self.next_state = State.GAME_OVER
            self.draw()
            self.shared.last_frame = self.shared.screen.copy()

        if self.shared.won:
            pygame.mouse.set_cursor(self.shared.target.ui_cursor)
            self.next_state = State.VICTORY
            self.draw()
            self.shared.last_frame = self.shared.screen.copy()

        if self.shared.king is not None:
            self.shared.king.update()
        self.light_rect.center = self.shared.target.gs_pos

    def draw(self):
        self.overlay.fill("black")
        # self.shared.screen.fill("black")
        self.game_surface.fill("seagreen")
        self.star_manager.draw()
        for citizen in self.shared.citizens:
            citizen.draw()

        if self.shared.king is not None:
            self.shared.king.draw()
        for monster in self.shared.monsters:
            monster.draw()
        self.shared.target.draw()
        if self.shared.winning:
            self.overlay.blit(self.light, self.light_rect)
            self.game_surface.blit(
                self.overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MIN
            )
        render_at(self.shared.screen, self.game_surface, "midright")
        self.shared.sidebar.draw()
