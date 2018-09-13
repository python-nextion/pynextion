
import pytest
from .config import PORT_DEFAULT
import time
from pynextion import PySerialNex
from pynextion.widgets import NexSlider
from pynextion.constants import Colour


@pytest.mark.parametrize("port", [PORT_DEFAULT])
def test_NexSlider(port):
    nexSerial = PySerialNex(port)

    nexSlider = NexSlider(nexSerial, "h0", cid=4)

    nexSerial.send("page pg_slider")
    time.sleep(0.1)

    nexSlider.value = 43691  # 0-65535

    time.sleep(1)

    # nexSlider.cursor.color = Colour.GRAY
    nexSlider.forecolor = Colour.GRAY

    time.sleep(1)

    w = 10
    nexSlider.cursor.width = w
    assert nexSlider.cursor.width == w

    time.sleep(1)

    h = 13
    nexSlider.cursor.height = h
    assert nexSlider.cursor.height == h

    time.sleep(1)

    nexSerial.close()
