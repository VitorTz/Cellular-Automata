from src.constants import Constants
from src.globals import Globals
from src.rule import Rule
import pygame


class Grid:

    __grid: list[list[int]]

    def __init__(self) -> None:
        self.reset()
    
    def reset(self) -> None:
        self.__grid = [None] * Constants.grid_lines
        for i in range(Constants.grid_lines):
            self.__grid[i] = [0 for _ in range(Constants.grid_columns)]
        
    def draw(self, alive_cells: list[tuple[int, int]]) -> None:
        rect = pygame.Rect(0, 0, Constants.cell_width, Constants.cell_height)
        for i, j in alive_cells:
            rect.left = j * rect.width
            rect.top = i * rect.height
            pygame.draw.rect(Globals.display, Constants.cell_color, rect)
    
    def main(self, rule: Rule) -> None:
        alive_cells: list[tuple[int, int]] = rule.run_rule(self.__grid)
        self.draw(alive_cells)