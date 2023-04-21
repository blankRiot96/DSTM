import asyncio

import pygame

from src.shared import Shared


class Game:
    def __init__(self) -> None:
        self.shared = Shared()
        self.win_init()
        from src.states import StateManager

        self.shared.dt = 0.0
        self.state_manager = StateManager()

    def win_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1024, 600))
        self.shared.screen = self.screen
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Don't Shoot the Monster!")
        pygame.display.set_icon(pygame.image.load("assets/monster.png"))
        # img = pygame.image.load("assets/target.png")
        # img = scale_by(img, 0.1)
        # center = img.get_rect().center
        # pygame.mouse.set_cursor(pygame.cursors.Cursor(center, img))

    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                raise SystemExit

        self.state_manager.update()
        self.shared.dt = self.clock.tick() / 1000
        self.shared.dt = min(self.shared.dt, 0.1)
        pygame.display.flip()

    def draw(self):
        self.screen.fill((100, 200, 100))
        self.state_manager.draw()
        # pygame.draw.rect(self.screen, "red", self.shared.grect, 3)

    async def run(self):
        while True:
            self.update()
            self.draw()
            await asyncio.sleep(0)


def main():
    game = Game()
    asyncio.run(game.run())


if __name__ == "__main__":
    main()
