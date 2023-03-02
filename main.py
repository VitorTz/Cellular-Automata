from src.generation import Generation
from src.constants import Constants
from src.globals import Globals
from src.menu import Menu
from sys import exit
import pygame


def init() -> None:
    """Inicia as variáveis globais necessárias para iniciar o programa"""
    pygame.init()
    pygame.font.init()
    Globals.display = pygame.display.set_mode(Constants.window_size)
    Globals.display_rect = Globals.display.get_rect()
    Globals.clock = pygame.time.Clock()
    Globals.rule_number = 0
    pygame.display.set_caption(Constants.window_title)


def close() -> None:
    """Fecha o programa"""
    pygame.quit()
    exit()


def check_events() -> None:
    """
    Atualiza as teclas do teclado pressionadas no loop atual e
    lida com a solicitação de fechar a janela e pausar o jogo.
    """
    Globals.pressed_keys.clear()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            close()
        elif e.type == pygame.KEYDOWN:
            Globals.pressed_keys.add(e.key)
            if e.key == Constants.pause_key:
                Globals.is_running = False


def count_frames() -> None:
    Globals.clock.tick(Constants.window_fps)
    Globals.frame += 1


def main() -> None:
    init()
    generation = Generation()
    menu = Menu(generation)
    while True:
        check_events()
        Globals.display.fill(Constants.window_bg_color)
        generation.main()  # Método main de generation só é executado caso Globals.is_running for True
        menu.main()  # Método main de manu só é executado caso Globals.is_running for False
        pygame.display.update()
        count_frames()


if __name__ == "__main__":
    main()
