from src.constants import Constants
from src.globals import Globals
import pygame



class Generation:

    __generation: list[list[int]]
    __index_current_line: int
  
    def __init__(self) -> None:
        self.reset()
    
    @property
    def generation(self) -> list[list[int]]:
        """Matriz que representa o estado atual da geração"""
        return self.__generation
    
    def reset(self) -> None:
        """Reseta a matriz das gerações e o index da linha atual"""
        l, c = Constants.grid_lines, Constants.grid_columns
        self.__generation = [[0 for _ in range(c)] for _ in range(l)]
        self.__generation[0][c//2] = 1
        self.__index_current_line = 0

    def move_up(self) -> None:
        """Move todas as linhas da matriz para cima caso seja necessário"""
        self.__index_current_line += 1
        if self.__index_current_line + 1 >= Constants.grid_lines:
            self.__generation = self.__generation[1:]
            self.__generation.append([0 for _ in range(Constants.grid_columns)])
            self.__index_current_line -= 1
    
    def draw(self) -> None:
        """Desenha as celulas vivas na tela"""
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
        """Executa  a regra escolhida"""
        bin_number: str = bin(Globals.rule_number)[2:].zfill(8)[::-1]
        patterns: dict[str, int] = {
            p: int(bin_number[i]) for i, p in enumerate(Constants.patterns)
        }
        line = self.__generation[self.__index_current_line]
        next_line = self.__generation[self.__index_current_line+1]
        for j, cell in enumerate(line):
            l, r = j-1, j+1
            if l < 0: l = -1
            if r >= Constants.grid_columns: r = 0
            cell_pattern = f"{line[l]}{cell}{line[r]}"
            next_state = patterns[cell_pattern]
            next_line[j] = next_state
        
    def main(self) -> None:
        """A regra é executada apenas quando o programa não está pausado"""
        if Globals.is_running:
            self.draw()
            self.apply_rule()
            self.move_up() 