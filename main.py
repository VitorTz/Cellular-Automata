from src.constants import Constants
from src.handle_events import HandleEvents
from src.globals import Globals
from src.grid import Grid
from src.menu import Menu
from src.rule import Rule
import pygame


def init() -> None:
    pygame.init()
    Globals.display = pygame.display.set_mode(Constants.window_size)
    pygame.display.set_caption(Constants.window_title)


def main() -> None:
    init()
    grid = Grid()
    rule = Rule(Constants.rule_number)
    menu = Menu()
    handle_events = HandleEvents(grid, rule, menu)
    while True:
        handle_events.main()
        Globals.display.fill(Constants.window_bg_color)
        grid.main(rule)
        pygame.display.update()
    

if __name__ == "__main__":
    main()