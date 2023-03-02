from src.generation import Generation
from src.constants import Constants
from src.globals import Globals
from typing import Callable
from pathlib import Path
from src import functions
import pygame


class Image:


    def __init__(self, image: Path | pygame.Surface, topleft: tuple[int, int]) -> None:
        self.image = image
        self.rect = self.image.get_rect(topleft=topleft)
    
    @property
    def image(self) -> pygame.Surface:
        return self.__image
    
    @image.setter
    def image(self, image: pygame.Surface | Path):
        if isinstance(image, pygame.Surface):
            self.__image = image
        elif isinstance(image, Path):
            self.__image = pygame.image.load(image).convert_alpha()
        else:
            raise ValueError()
    
    def draw(self) -> None:
        Globals.display.blit(self.image, self.rect)
    

class Text:

    def __init__(self, text: str, topleft: tuple[int, int]) -> None:
        self.__text = text
        self.__image = Image(self.__convert_text_to_pygame_image(text), topleft)
    
    @property
    def text(self) -> str:
        return self.__text
    
    @text.setter
    def text(self, text: str):
        self.__text = text
        self.__image.image = self.__convert_text_to_pygame_image(self.__text)
    
    def __convert_text_to_pygame_image(self, text: str) -> pygame.Surface:
        return pygame.font.Font(Constants.font, Constants.font_size).render(
            text, True, Constants.font_color
        )

    def draw(self) -> None:
        self.__image.draw()


class Button:

    """
        Representa um botão em formato de imagem.
        Recebe duas imagens, uma para seu estado padrão
        e outra para seu estado hover. 
        Também recebe uma função que deve ser acionada
        com o clique do usuário no botão.

    """

    def __init__(
            self, 
            image_default: Path, 
            image_hover: Path, 
            topleft: tuple[int, int],
            click_function: Callable
        ) -> None:
        self.__image_default = Image(image_default, topleft)
        self.__image_hover = Image(image_hover, topleft)
        self.__click_function = click_function
    
    def __is_on_hover(self) -> bool:
        return self.__image_default.rect.collidepoint(pygame.mouse.get_pos())

    def __is_clicked(self) -> bool:
        return pygame.mouse.get_pressed()[0] and self.__is_on_hover()
    
    def __draw(self) -> None:
        if self.__is_on_hover():
            self.__image_hover.draw()
        else:
            self.__image_default.draw()
    
    def __handle_click(self) -> None:
        if callable(self.__click_function) and self.__is_clicked():
            self.__click_function()
        
    def run(self) -> None:
        self.__draw()
        self.__handle_click()


class HandleKeyboard:

    """
        Lida com o pressionamento das teclas númericas
        de 1 a 9 no teclado e também com a tecla backspace. 
        Esta classe tem como função receber o número da regra a ser executada, 
        um número de regra válido está entre 0 e 255.
    """

    def __init__(self, text: Text) -> None:
        self.__rule_number = text  # Responsável por guardar o número da regra
        self.__bar = "|"  # Barra que deve ficar "piscando", indicando que o usuário deve digitar algo
    
    @property
    def number(self) -> str:
        """Número digitado pelo usuário"""
        return self.__rule_number.text.replace(self.__bar, "")

    def __handle_backspace(self) -> None:
        """Remove o ultimo digito da regra caso o backspace seja pressionado"""
        if Constants.backspace in Globals.pressed_keys and self.number:
            self.__rule_number.text = self.number[:-1]
    
    def __add_digit(self, digit: str) -> None:
        """
        Adiciona um digito no final do número. 
        Apenas se o número não conta com 3 digitos
        """
        if digit and len(self.number) < 3:
            self.__rule_number.text = self.number + digit
    
    def __blink_bar(self) -> None:
        """Faz a barra 'picar' a cada 20 frames"""
        if Globals.frame % 20 == 0:
            if self.__bar in self.__rule_number.text:
                self.__rule_number.text = self.number
            else:
                self.__rule_number.text = self.number + self.__bar

    def main(self) -> None:
        self.__handle_backspace()
        self.__add_digit(functions.get_last_digit_pressed())
        self.__blink_bar()


class Menu:


    """
        O menu possui:
        Um campo de texto para o usuário entrar com o número da regra
        Botão Start para começar a executar a regra escolhida
        Botão Reset para reiniciar a execução da regra
        Botão Screenshot para tirar uma captura de tela
    """


    def __init__(self, generation: Generation) -> None:
        self.__background_image = Image(Constants.menu_bg, (0, 0))
        self.__background_image.rect.center = Globals.display_rect.center
        self.__start_btn = Button(
            Constants.start_btn, 
            Constants.start_btn_hover, 
            Constants.start_btn_topleft,
            self.__start
        )
        self.__reset_btn = Button(
            Constants.reset_btn, 
            Constants.reset_btn_hover, 
            Constants.reset_btn_topleft,
            self.__reset
        )
        self.__screenshot_btn = Button(
            Constants.screenshot_btn,
            Constants.screenshot_btn_hover,
            Constants.screenshot_btn_topleft,
            lambda : functions.take_screenshot(self.__generation.generation)
        )
        self.__rule_number = Text("", Constants.menu_text_topleft)
        self.__handle_keyboard = HandleKeyboard(self.__rule_number)
        self.__generation = generation
    
    def __start(self) -> None:
        """
            Verifica se o número digitado pelo usuário é válido,
            caso sim inicia a execução da regra.
        """
        try:
            rule_number = int(self.__handle_keyboard.number)
            if not (0 <= rule_number <= 255):
                raise ValueError()
            if rule_number != Globals.rule_number:
                Globals.rule_number = rule_number
                self.__reset()
            Globals.is_running = True
        except Exception:
            pass

    def __reset(self) -> None:
        self.__generation.reset()
        Globals.is_running = True
    
    def main(self) -> None:
        """O menu funciona apenas quando nenhuma regra está sendo executada"""
        if not Globals.is_running:
            self.__background_image.draw()
            self.__handle_keyboard.main()
            self.__rule_number.draw()
            self.__start_btn.run()
            self.__reset_btn.run()
            self.__screenshot_btn.run()