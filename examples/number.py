import pytest
from .config import PORT_DEFAULT
import time
from pynextion import PySerialNex
from pynextion.widgets import NexNumber
from pynextion.constants import Colour


@pytest.mark.parametrize("port", [PORT_DEFAULT])
def test_NexNumber(port):
    nexSerial = PySerialNex(port)

    nexNumber = NexNumber(nexSerial, "n0", cid=1)

    nexSerial.send("page pg_num")

    time.sleep(1)
    nexNumber.value = 1
    time.sleep(1)
    nexNumber.value = 2
    nexNumber.backcolor = Colour.RED
    nexNumber.forecolor = Colour.WHITE

    time.sleep(1)
    assert nexNumber.value == 2
    time.sleep(1)
    nexNumber.value = 3
    nexNumber.backcolor = Colour.WHITE
    nexNumber.forecolor = Colour.RED
    time.sleep(1)

    """
    n = typemax(Int32)
    # how to get max and min val of C integers (from Python)
    # see also https://stackoverflow.com/questions/9860588/maximum-value-for-long-integer/9860812

    nexNumber.value = n
    time.sleep(1)
    assert nexNumber.value == n
    """

    """
    n = typemin(Int32)
    nexNumber.value = n
    time.sleep(1)
    assert nexNumber.value == n
    """

    n = -2
    nexNumber.value = n
    time.sleep(1)
    assert nexNumber.value == n

    nexSerial.close()
