import pytest
from .config import PORT_DEFAULT
import time
from pynextion import PySerialNex
from pynextion.widgets import NexRadio


@pytest.mark.parametrize("port", [PORT_DEFAULT])
def test_NexRadio(port):
    nexSerial = PySerialNex(port)

    nexRadio0 = NexRadio(nexSerial, "r0", cid=8)
    nexRadio1 = NexRadio(nexSerial, "r1", cid=9)
    nexRadio2 = NexRadio(nexSerial, "r2", cid=10)

    nexSerial.send("page pg_dsb_chk_rad")

    nexRadio0.value = False
    nexRadio1.value = False
    nexRadio2.value = False

    assert not nexRadio0.value

    time.sleep(1)

    nexRadio0.value = True

    assert nexRadio0.value

    time.sleep(1)

    nexRadio0.value = False

    assert not nexRadio0.value

    time.sleep(1)

    nexSerial.close()
