from enum import Enum, auto


class State(Enum):
    MENU = auto()
    GAME = auto()
    GAME_OVER = auto()
