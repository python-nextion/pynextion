import pytest
from .config import PORT_DEFAULT
import time
from pynextion import PySerialNex
from pynextion.widgets import NexButton, NexNumber
from pynextion.constants import Colour


@pytest.mark.parametrize("port", [PORT_DEFAULT])
def test_pages(port):
    nexSerial = PySerialNex(port)

    nexButtonPlus = NexButton(nexSerial, "b0", cid=1)
    nexNumber0 = NexNumber(nexSerial, "n0", cid=2)
    nexButtonMinus = NexButton(nexSerial, "b1", cid=3)
    nexButtonEnter = NexButton(nexSerial, "b2", cid=4)  # noqa: F841

    nexSerial.send("page pg_but")

    nexButtonPlus.backcolor = Colour.GREEN
    nexButtonMinus.backcolor = Colour.RED

    # nexNumber0.value = value
    value = nexNumber0.value
    while True:
        time.sleep(0.2)
        new_value = nexNumber0.value
        if new_value != value:
            value = new_value
            print(value)

    nexSerial.close()
