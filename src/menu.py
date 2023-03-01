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
        self.__image = Image(self.__get_img(text), topleft)
    
    @property
    def text(self) -> str:
        return self.__text
    
    @text.setter
    def text(self, text: str):
        self.__text = text
        self.__image.image = self.__get_img(self.__text)
    
    def __get_img(self, text: str) -> pygame.Surface:
        return pygame.font.Font(Constants.font, Constants.font_size).render(
            text, True, Constants.font_color
        )

    def draw(self) -> None:
        self.__image.draw()


class Button:

    def __init__(
            self, 
            image_default: Path, 
            image_hover: Path, 
            topleft: tuple[int, int],
            click_event: Callable
        ) -> None:
        self.__image_default = Image(image_default, topleft)
        self.__image_hover = Image(image_hover, topleft)
        self.__click_event = click_event
    
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
        if callable(self.__click_event) and self.__is_clicked():
            self.__click_event()
        
    def run(self) -> None:
        self.__handle_click()
        self.__draw()


class HandleKeyboard:


    def __init__(self, text: Text) -> None:
        self.__text = text
        self.__bar = "|"
    
    @property
    def text_input(self) -> str:
        return self.__text.text.replace(self.__bar, "")

    def __handle_backspace(self) -> None:
        if Constants.backspace in Globals.pressed_keys:
            if self.text_input:
                self.__text.text = self.text_input[:-1]
    
    def __add_digit(self, digit: str) -> None:
        if len(self.text_input) < 3 and digit:
            self.__text.text = self.text_input + digit
    
    def __blink_bar(self) -> None:
        if Globals.frame % 20 == 0:
            if self.__bar in self.__text.text:
                self.__text.text = self.text_input
            else:
                self.__text.text = self.text_input + self.__bar

    def main(self) -> None:
        self.__handle_backspace()
        self.__add_digit(functions.get_last_digit_pressed())
        self.__blink_bar()


class Menu:


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
        self.__text_input = Text("", Constants.menu_text_topleft)
        self.__handle_keyboard = HandleKeyboard(self.__text_input)
        self.__generation = generation
    
    def __start(self) -> None:
        try:
            rule_number = int(self.__handle_keyboard.text_input)
            if not (0 <= rule_number <= 255):
                raise ValueError()
            Globals.is_running = True
            if rule_number != Globals.rule_number:
                Globals.rule_number = rule_number
                self.__reset()
        except Exception:
            pass

    def __reset(self) -> None:
        self.__generation.reset()
        Globals.is_running = True
    
    def __run_btns(self) -> None:
        self.__start_btn.run()
        self.__reset_btn.run()
        self.__screenshot_btn.run()

    def main(self) -> None:
        if not Globals.is_running:
            self.__background_image.draw()
            self.__handle_keyboard.main()
            self.__text_input.draw()
            self.__run_btns()