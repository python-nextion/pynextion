import pytest
from .config import PORT_DEFAULT
import time
from pynextion import PySerialNex
from pynextion.constants import (
    Colour,
    Alignment,
    Background
)
from pynextion.resources import (
    Font,
    Picture
)
from pynextion.draw import (
    cls,
    circle,
    line,
    rectangle,
    xstr,
    picture
)


LCD_WIDTH, LCD_HEIGHT = 480, 320
DEFAULT_COLOUR = Colour.WHITE
IMG_WIDTH, IMG_HEIGHT = 200, 135


@pytest.mark.parametrize("port", [PORT_DEFAULT])
def test_draw(port):
    nexSerial = PySerialNex(port)

    nexSerial.send("page0")
    cls(nexSerial, DEFAULT_COLOUR)

    def print_several_lines(nexSerial, lcd_width=LCD_WIDTH, color1="WHITE", color2="BLACK"):
        def swap(x, y):
            return y, x

        x, y = 0, 10
        w, h = lcd_width, 30
        font = Font(0)
        fontcolor = color1
        backcolor = color2
        xcenter = Alignment.Horizontal.CENTRE  # NONE/LEFT/CENTRE/RIGHT
        ycenter = Alignment.Vertical.CENTRE  # NONE/UP/CENTRE/DOWN
        sta = Background.SOLIDCOLOUR  # NONE/CROPIMAGE/SOLIDCOLOUR/IMAGE/NOBACKCOLOUR

        rows = [
            "Hello Python!",
            "",
            "This is Nextion",
            "",
            "I'm an intelligent display",
            "",
            "",
            "",
            "https://github.com/scls19fr",
            "/pynextion"
        ]
        for row in rows:
            print(nexSerial, row, x, y, w, h, font, fontcolor, backcolor, xcenter, ycenter, sta)
            xstr(nexSerial, row, x, y, w, h, font, fontcolor, backcolor, xcenter, ycenter, sta)
            y = y + h
            fontcolor, backcolor = swap(fontcolor, backcolor)

    def diagonal_line(nexSerial, lcd_width=LCD_WIDTH, lcd_height=LCD_HEIGHT):
        x1, y1 = 0, 0
        x2, y2 = lcd_width, lcd_height
        colour = Colour.BLUE
        line(nexSerial, x1, y1, x2, y2, colour)

    def circle_frame_fill(nexSerial, lcd_width=LCD_WIDTH, lcd_height=LCD_HEIGHT, delay=1):
        x = int(round(lcd_width / 2))
        y = int(round(lcd_height / 2))
        r = 100
        colour = Colour.BLUE
        circle(nexSerial, x, y, r, colour)
        time.sleep(delay)
        circle(nexSerial, x, y, r, colour, Background.SOLIDCOLOUR)

    def clear_screen_color_france(nexSerial, delay=1):
        cls(nexSerial, Colour.BLUE)
        time.sleep(delay)
        cls(nexSerial, Colour.WHITE)
        time.sleep(delay)
        cls(nexSerial, Colour.RED)

    def france_flag(nexSerial, lcd_width=LCD_WIDTH, lcd_height=LCD_HEIGHT):
        w, h = int(round(lcd_width / 3)), lcd_height
        x1, y1 = 0, 0
        y2 = h
        x2 = x1 + w
        colour = Colour.BLUE
        rectangle(nexSerial, x1, y1, x2, y2, colour, Background.SOLIDCOLOUR)
        x1 = x1 + 2 * w
        x2 = x1 + w
        colour = Colour.RED
        rectangle(nexSerial, x1, y1, x2, y2, colour, Background.SOLIDCOLOUR)

    def rectangle_frame_fill(nexSerial, lcd_width=LCD_WIDTH, lcd_height=LCD_HEIGHT):
        w, h = 120, 80
        x1 = int(round((lcd_width - w) / 2))
        y1 = int(round((lcd_height - h) / 2))
        x2 = x1 + w
        y2 = y1 + h
        colour = Colour.RED
        rectangle(nexSerial, x1, y1, x2, y2, colour)
        time.sleep(1)
        rectangle(nexSerial, x1, y1, x2, y2, colour, Background.SOLIDCOLOUR)

    def picture_example(nexSerial, lcd_width=LCD_WIDTH, lcd_height=LCD_HEIGHT, img_width=IMG_WIDTH, img_height=IMG_HEIGHT, delay=0.5):
        x = int(round((lcd_width - img_width) / 2))
        y = int(round((lcd_height - img_height) / 2))
        for picid in range(5):
            picture(nexSerial, x, y, Picture(picid))
            time.sleep(delay)

    cls(nexSerial)

    print_several_lines(nexSerial)
    time.sleep(2)

    cls(nexSerial, DEFAULT_COLOUR)
    diagonal_line(nexSerial)

    time.sleep(2)
    cls(nexSerial)

    circle_frame_fill(nexSerial)

    time.sleep(2)
    cls(nexSerial)

    clear_screen_color_france(nexSerial)

    time.sleep(2)
    cls(nexSerial)

    france_flag(nexSerial)

    time.sleep(2)
    cls(nexSerial)
    time.sleep(1)

    rectangle_frame_fill(nexSerial)

    time.sleep(2)
    cls(nexSerial)

    picture_example(nexSerial)

    nexSerial.close()
