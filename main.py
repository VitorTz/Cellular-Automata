from src.constants import Constants
from src.globals import Globals
from src.grid import Grid
from src.rule import Rule
from sys import exit
import pygame


def init() -> None:
    pygame.init()
    Globals.display = pygame.display.set_mode(Constants.window_size)
    Globals.clock = pygame.time.Clock()
    pygame.display.set_caption(Constants.window_title)


def close() -> None:
    pygame.quit()
    exit()


def reset(grid: Grid, rule: Rule, rule_number: int) -> None:
    grid.reset()
    rule.reset(rule_number)


def check_events() -> None:
    Globals.keys.clear()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            close()
        elif e.type == pygame.KEYDOWN:
            Globals.keys[e.key] = True


def main() -> None:
    init()
    grid = Grid()
    rule = Rule(Constants.rule_number)
    while True:
        check_events()
        Globals.display.fill(Constants.window_bg_color)
        grid.main(rule)
        pygame.display.update()
        Globals.clock.tick(Constants.window_fps)
    

if __name__ == "__main__":
    main()