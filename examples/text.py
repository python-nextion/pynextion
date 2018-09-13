
import pytest
from .config import PORT_DEFAULT
import time
from pynextion import PySerialNex
from pynextion.widgets import NexText
from pynextion.constants import Colour, Alignment
from pynextion.resources import Font


@pytest.mark.parametrize("port", [PORT_DEFAULT])
def test_NexSlider(port):
    nexSerial = PySerialNex(port)

    print("Init")
    nexSerial.init()

    print("Create objects")
    # nexText = NexText(nexSerial, "t1", pid=2, cid=1)
    # nexText = NexText(nexSerial, "t1")
    nexText = NexText(nexSerial, "t1", cid=1)

    print("Reset")
    nexSerial.reset()

    time.sleep(1)

    nexSerial.send("page pg_text")

    time.sleep(1)

    msg = "Hello"
    nexText.text = msg

    time.sleep(1)
    assert nexText.text == msg

    time.sleep(0.5)

    nexText.backcolor = Colour.BLUE
    nexText.text = "1"

    time.sleep(0.5)

    nexText.backcolor = Colour.WHITE
    nexText.text = "2"

    time.sleep(0.5)

    nexText.backcolor = Colour.RED
    nexText.text = "3"

    time.sleep(0.5)

    nexText.text = "Bye nexText"

    time.sleep(0.5)

    nexText.visible = False
    nexText.backcolor = Colour.WHITE

    time.sleep(2)

    nexText.visible = True

    time.sleep(0.5)

    nexText.alignment.horizontal = Alignment.Horizontal.RIGHT
    nexText.alignment.vertical = Alignment.Vertical.DOWN
    nexText.forecolor = Colour.BLUE

    # Change fontid from 0 to 1
    nexText.font = Font(1)

    # nexSerial.reset()
    # time.sleep(0.5)

    nexSerial.close()
