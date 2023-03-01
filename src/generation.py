from src.constants import Constants
from src.globals import Globals
import pygame



class Generation:

    __generation: list[list[int]]
    __index_current_line: int
    __patterns = [
        "000",
        "001",
        "010",
        "011",
        "100",
        "101",
        "110",
        "111"
    ]

    def __init__(self) -> None:
        self.reset()
    
    @property
    def generation(self) -> list[list[int]]:
        return self.__generation

    def move_up(self) -> None:
        self.__index_current_line += 1
        if self.__index_current_line + 1 >= Constants.grid_lines:
            self.__generation = self.__generation[1:]
            self.__generation.append(
                [0 for _ in range(Constants.grid_columns)]
            )
            self.__index_current_line -= 1
    
    def reset(self) -> None:
        l, c = Constants.grid_lines, Constants.grid_columns
        self.__generation = [[0 for _ in range(c)] for _ in range(l)]
        self.__generation[0][c//2] = 1
        self.__index_current_line = 0
    
    def draw(self) -> None:
        w = Constants.cell_width
        h = Constants.cell_height
        for i, line in enumerate(self.generation[:self.__index_current_line]):
            for j, cell in enumerate(line):
                if cell:
                    pygame.draw.rect(
                        Globals.display,
                        Constants.cell_color,
                        (j * w, i * h, w, h)
                    )
    
    def apply_rule(self) -> None:
        bin_number: str = bin(Globals.rule_number)[2:].zfill(8)[::-1]
        pattern_by_state: dict[str, int] = {
            pattern: int(bin_number[i]) for i, pattern in enumerate(Constants.patterns)
        }
        line = self.__generation[self.__index_current_line]
        next_line = self.__generation[self.__index_current_line+1]
        for j, cell in enumerate(line):
            l, r = j-1, j+1
            if l < 0: l = -1
            if r >= Constants.grid_columns: r = 0
            pattern = f"{line[l]}{cell}{line[r]}"
            new_state = pattern_by_state[pattern]
            next_line[j] = new_state
        
    def main(self) -> None:
        if Globals.is_running:
            self.draw()
            self.apply_rule()
            self.move_up() 