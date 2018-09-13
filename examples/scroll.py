
import pytest
from .config import PORT_DEFAULT
import time
from pynextion import PySerialNex
from pynextion.widgets import NexPage, NexScrollText


@pytest.mark.parametrize("port", [PORT_DEFAULT])
def test_NexScrollText(port):
    nexSerial = PySerialNex(port)
    # nexSerial.write("page pg_scroll")

    nexPage = NexPage(nexSerial, "pg_scroll", pid=5)
    nexPage.show()

    nexScrollText = NexScrollText(nexSerial, "g0", pid=1)
    msg = "Hello Nextion!"
    nexScrollText.text = msg
    assert nexScrollText.text == msg
    time.sleep(10)

    nexSerial.close()
