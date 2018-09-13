
import pytest
from .config import PORT_DEFAULT
import time
from pynextion import PySerialNex
from pynextion.widgets import NexGauge
from pynextion.constants import Colour


@pytest.mark.parametrize("port", [PORT_DEFAULT])
def test_gauge(port):
    nexSerial = PySerialNex(port)

    nexGauge = NexGauge(nexSerial, "z0", cid=3)

    nexGauge.backcolor = Colour.WHITE
    nexGauge.forecolor = Colour.RED

    nexGauge.width = 3  # 0-5
    # nexGauge.pointer.width = 3  # 0-5

    # for angle in range(30, 360 + 30, 30)
    #     time.sleep(1)
    #     nexGauge.value = angle

    for angle in range(0, 360 + 6, 6):
        time.sleep(0.1)
        nexGauge.value = (angle + 90) % 360

    time.sleep(1)

    assert nexGauge.value == 90

    nexSerial.close()
