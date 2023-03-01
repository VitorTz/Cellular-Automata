from pygame import K_SPACE


class Constants:


    # window
    window_width = 1280
    window_height = 720
    window_size = (window_width, window_height)
    window_title = "Cellular Automata"
    window_bg_color = (27, 29, 38)

    # cell
    cell_color = (246, 167, 59)
    cell_width = 1
    cell_height = 1
    
    # grid
    grid_lines = window_height // cell_height
    grid_columns = window_width // cell_width

    # rules
    rule_number = 1

    # keyboard
    reset_key: int = K_SPACE