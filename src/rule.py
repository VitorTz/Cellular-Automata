from typing import Callable


class Rule:

    __rules: dict[int, Callable] = {

    }
    __current_rule: Callable | None = None

    def __init__(self, number: int) -> None:
        self.reset(number)
    
    def reset(self, number: int) -> None:
        self.__current_rule = self.__rules.get(number)
    
    def run_rule(self, grid: list[list[int]]) -> list[tuple[int, int]]:
        return []
        return self.__current_rule(grid)