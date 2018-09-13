import pytest
from .config import PORT_DEFAULT
import time
from pynextion import PySerialNex
from pynextion.widgets import NexProgressBar
from pynextion.constants import Colour


@pytest.mark.parametrize("port", [PORT_DEFAULT])
def test_NexProgressBar(port):
    nexSerial = PySerialNex(port)

    nexProgressBar = NexProgressBar(nexSerial, "j0", cid=1)

    nexSerial.send("page pg_pbar")

    time.sleep(1)

    nexProgressBar.backcolor = Colour.GRAY
    nexProgressBar.forecolor = Colour.GREEN
    nexProgressBar.value = 30

    with pytest.raises(Exception):
        nexProgressBar.value = 105  # should raise error because value must be in 0-100

    with pytest.raises(Exception):
        nexProgressBar.value = -1  # should raise error because value must be in 0-100

    time.sleep(1)

    nexSerial.close()
