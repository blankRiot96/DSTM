import typing as t

import pygame

from src.gameover import GameOver
from src.gamestate import GameState
from src.menustate import MenuState
from src.state_enums import State
from src.tutorialstate import TutorialState
from src.victorystate import VictoryState


class StateLike(t.Protocol):
    next_state: State | None

    def update(self):
        ...

    def draw(self):
        ...


class StateManager:
    def __init__(self) -> None:
        self.state_dict: dict[State, StateLike] = {
            State.MENU: MenuState,
            State.GAME: GameState,
            State.GAME_OVER: GameOver,
            State.TUTORIAL: TutorialState,
            State.VICTORY: VictoryState,
        }
        self.songs = {
            State.MENU: "assets/audio/main-menu-bgm.wav",
            State.TUTORIAL: "assets/audio/game-bgm.wav",
            State.GAME: "assets/audio/game-bgm.wav",
            State.GAME_OVER: "assets/audio/game-over-bgm.wav",
            State.VICTORY: "assets/audio/game-bgm.wav",
        }
        self.state_enum = State.MENU
        self.state_obj: StateLike = self.state_dict.get(self.state_enum)()

    @property
    def state_enum(self) -> State:
        return self.__state_enum

    @state_enum.setter
    def state_enum(self, next_state: State) -> None:
        self.__state_enum = next_state
        self.state_obj: StateLike = self.state_dict.get(self.__state_enum)()
        pygame.mixer.music.load(self.songs[next_state])
        pygame.mixer.music.play(fade_ms=2500, loops=-1)

    def update(self):
        self.state_obj.update()
        if self.state_obj.next_state is not None:
            self.state_enum = self.state_obj.next_state

    def draw(self):
        self.state_obj.draw()
