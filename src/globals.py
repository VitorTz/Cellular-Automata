import pygame


class Globals:

    # late init
    display: pygame.Surface
    display_rect: pygame.Rect
    clock: pygame.time.Clock
    rule_number: int

    # keyboard keys
    pressed_keys: set[int] = set()
    
    is_running = False
    frame: int = 0


