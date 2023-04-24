import random

import pygame

from src.citizen import Citizen, CitizenType
from src.shared import Shared
from src.state_enums import State
from src.utils import get_font, render_at, scale_by


class Slide1:
    FONT_1 = get_font("assets/fonts/bold1.ttf", 32)
    FONT_2 = get_font("assets/fonts/bold1.ttf", 21)

    def __init__(self) -> None:
        self.text_surf = self.FONT_2.render("TARGET", True, "white")
        self.shared = Shared()
        self.gen_target_surf()

        self.ex_surf = Citizen.IMAGES[CitizenType.GREEN]
        self.ex_surf = scale_by(self.ex_surf, 2)
        self.ex_rect = self.ex_surf.get_rect(center=(400, 300))

        self.target_image = pygame.image.load("assets/target.png").convert_alpha()
        self.target_image = scale_by(self.target_image, 0.25)
        self.target_pos = pygame.Vector2(
            30, random.randrange(self.shared.SRECT.height - 100)
        )
        self.or_pos = self.target_pos.copy()
        self.trect = self.target_image.get_rect(center=self.target_pos)
        self.alpha = 0

        self.instruction_surf = self.FONT_1.render(
            """Drag the target cursor to the target,\n
      Click on them to gain score!""",
            True,
            "white",
        )

    def gen_target_surf(self):
        self.target_surf = pygame.Surface((100, 120), pygame.SRCALPHA)
        pygame.draw.rect(
            self.target_surf, "white", (0, 0, *self.target_surf.get_size()), 5
        )
        render_at(self.target_surf, self.text_surf, "midtop", (0, 10))
        render_at(
            self.target_surf, Citizen.IMAGES[CitizenType.GREEN], "midbottom", (0, -15)
        )
        self.target_surf = scale_by(self.target_surf, 2)

    def update(self):
        self.target_pos.move_towards_ip(self.ex_rect.center, 180 * self.shared.dt)
        self.trect = self.target_image.get_rect(center=self.target_pos)

        if self.target_pos == self.ex_rect.center:
            self.alpha = 0
            self.target_pos = self.or_pos.copy()
            self.target_pos.y = random.randrange(self.shared.SRECT.height - 100)

        if self.alpha >= 255:
            self.alpha = 255
        else:
            self.alpha += 75 * self.shared.dt

        self.target_image.set_alpha(self.alpha)

    def draw(self):
        render_at(self.shared.screen, self.target_surf, "center", (-350, 0))

        self.shared.screen.blit(self.ex_surf, self.ex_rect)
        self.shared.screen.blit(self.target_image, self.trect)

        render_at(self.shared.screen, self.instruction_surf, "center", (200, 0))


def create_from_messages(messages: str, font: pygame.font.Font) -> list[pygame.Surface]:
    return [font.render(message, True, "white") for message in messages]


class TutorialState:
    FONT_1 = get_font("assets/fonts/bold1.ttf", 32)

    def __init__(self) -> None:
        self.shared = Shared()
        self.next_state = None
        self.slides = (Slide1(),)
        self.__current_slide_index = 0
        self.current_slide = self.slides[self.__current_slide_index]
        self.messages = [
            "< TUTORIAL >",
            "Press ENTER to skip",
            "Previous slide -> LEFT key",
            "Next slide -> RIGHT key",
        ]
        self.surfaces = create_from_messages(self.messages, self.FONT_1)

    @property
    def current_slide_index(self):
        return self.__current_slide_index

    @current_slide_index.setter
    def current_slide_index(self, val):
        self.__current_slide_index = val
        self.current_slide = self.slides[self.__current_slide_index]

    def on_slide_change(self, value: int):
        possible_index = self.current_slide_index + value
        if possible_index < 0:
            possible_index = len(self.slides) - 1
        if possible_index == len(self.slides):
            possible_index = 0

        self.current_slide_index = possible_index

    def read_keys(self):
        for event in self.shared.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.next_state = State.GAME
                elif event.key == pygame.K_LEFT:
                    self.on_slide_change(-1)
                elif event.key == pygame.K_RIGHT:
                    self.on_slide_change(1)

    def update(self):
        self.current_slide.update()
        self.read_keys()

    def draw_general_info(self):
        for index, surf in enumerate(self.surfaces):
            y_offset = (self.FONT_1.get_height() + 3) * index
            render_at(self.shared.screen, surf, "midtop", (0, y_offset))

    def draw(self):
        self.shared.screen.fill("black")
        self.current_slide.draw()
        self.draw_general_info()
