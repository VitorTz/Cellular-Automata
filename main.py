from src.generation import Generation
from src.constants import Constants
from src.globals import Globals
from src.menu import Menu
from sys import exit
import pygame


AliveCells = list[tuple[int, int]]


def init() -> None:
    pygame.init()
    Globals.display = pygame.display.set_mode(Constants.window_size)
    Globals.display_rect = Globals.display.get_rect()
    Globals.clock = pygame.time.Clock()
    pygame.display.set_caption(Constants.window_title)


def close() -> None:
    pygame.quit()
    exit()


def check_events() -> None:
    Globals.pressed_keys.clear()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            close()
        elif e.type == pygame.KEYDOWN:
            Globals.pressed_keys.add(e.key)
            if e.key == Constants.pause_key:
                Globals.is_running = False


def count_frames() -> None:
    Globals.clock.tick(120)
    Globals.frame += 1


def main() -> None:
    init()
    generation = Generation()
    menu = Menu(generation)
    while True:
        check_events()
        Globals.display.fill(Constants.window_bg_color)
        generation.main()
        menu.main()
        pygame.display.update()
        count_frames()


if __name__ == "__main__":
    main()
