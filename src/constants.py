from pygame import K_SPACE, K_BACKSPACE, K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9
from pathlib import Path


class Constants:


    # window
    window_width = 1280
    window_height = 720
    window_size = (window_width, window_height)
    window_title = "Cellular Automata"
    window_bg_color = (27, 29, 38)

    # cell
    cell_color = (246, 167, 59)
    cell_width = 2
    cell_height = 2
    
    # grid
    grid_lines = window_height // cell_height
    grid_columns = window_width // cell_width


    patterns = [
        "000",
        "001",
        "010",
        "011",
        "100",
        "101",
        "110",
        "111"
    ]

    # keyboard
    pause_key: int = K_SPACE
    backspace: int = K_BACKSPACE
    digits: dict[int, str] = {
        K_0: "0",
        K_1: "1",
        K_2: "2",
        K_3: "3",
        K_4: "4",
        K_5: "5",
        K_6: "6",
        K_7: "7",
        K_8: "8",
        K_9: "9"
    }

    # menu
    menu_bg = Path("res/menu.png")
    
    start_btn = Path("res/start-btn.png")
    start_btn_hover = Path("res/start-btn_hover.png")
    start_btn_topleft = (524, 331)

    reset_btn = Path("res/reset-btn.png")
    reset_btn_hover = Path("res/reset-btn_hover.png")
    reset_btn_topleft = (643, 331)

    screenshot_btn = Path("res/screenshot_btn.png")
    screenshot_btn_hover = Path("res/screenshot_btn_hover.png")
    screenshot_btn_topleft = (524, 384)
    screenshot_folder = Path("screenshot")

    font = Path("res/JetBrainsMono-Regular.ttf")
    font_size = 20
    font_color = cell_color
    menu_text_topleft = (706, 292)

