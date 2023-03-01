from src.constants import Constants
from src.globals import Globals
from datetime import datetime
from pathlib import Path
from PIL import Image


def get_last_digit_pressed() -> str:
        digits: dict[int, str] = Constants.digits
        pressed_keys: set[int] = Globals.pressed_keys
        try:
            digit: str = [digits[d] for d in pressed_keys if d in digits.keys()][0]
            return digit
        except Exception:
            return ""
        

def take_screenshot(generation: list[list[int]]) -> None:
    screenshot_dir: Path = Constants.screenshot_folder
    if not screenshot_dir.exists():
        screenshot_dir.mkdir()
    image = Image.new("RGB", (Constants.grid_columns, Constants.grid_lines), Constants.window_bg_color)
    for i, line in enumerate(generation):
        for j, cell in enumerate(line):
            if cell:
                image.putpixel((j, i), Constants.cell_color)
            
    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y_%H:%M:%S")
    image.save(screenshot_dir / f"{date_time}.png")