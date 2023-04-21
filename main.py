import asyncio

import pygame


class Game:
    def __init__(self) -> None:
        self.win_init()

    def win_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1024, 600))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Don't Shoot the Monster!")

    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                raise SystemExit

        self.clock.tick()
        pygame.display.flip()

    def draw(self):
        self.screen.fill("seagreen")
        pygame.draw.rect(self.screen, "red", (150, 150, 50, 50))

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
