from src.constants import Constants
from src.globals import Globals
from src.grid import Grid
from src.menu import Menu
from src.rule import Rule
from typing import Callable
from sys import exit
import pygame


class HandleEvents:

    __keys_map: dict[int, Callable] = {

    }

    def __init__(self, grid: Grid, rule: Rule, menu: Menu) -> None:
        self.__grid = grid
        self.__rule = rule
        self.__menu = menu
    
    def handle_keyboard(self, key: int) -> None:
        f: Callable | None = self.__keys_map.get(key)
        if callable(f):
            f()
    
    def main(self) -> None:
        Globals.keys.clear()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif e.type == pygame.KEYDOWN:
                Globals.keys[e.key] = True
                self.handle_keyboard(e.key)
