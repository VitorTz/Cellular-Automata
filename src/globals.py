import pygame


class Globals:


    display: pygame.Surface
    display_rect: pygame.Rect
    clock: pygame.time.Clock

    pressed_keys: set[int] = set()

    is_running = False
    frame: int = 0

    rule_number = 73

