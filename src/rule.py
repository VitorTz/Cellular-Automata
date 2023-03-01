from typing import Callable
from src.constants import Constants
from random import randint


class Rule:

    __rules: dict[int, Callable] = {

    }
    __current_rule: Callable | None = None

    def __init__(self, number: int) -> None:
        self.reset(number)
    
    def reset(self, number: int) -> None:
        self.__current_rule = self.__rules.get(number)
    
    def run_rule(self, grid: list[list[int]]) -> list[tuple[int, int]]:
        return [(randint(1, Constants.grid_lines), randint(1, Constants.grid_columns)) for i in range(100000)]
        return self.__current_rule(grid)