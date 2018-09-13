import pytest
from .config import PORT_DEFAULT
import time
from pynextion import PySerialNex
from pynextion.widgets import NexCheckbox


@pytest.mark.parametrize("port", [PORT_DEFAULT])
def test_NexCheckbox(port):
    nexSerial = PySerialNex(port)

    nexCheckbox0 = NexCheckbox(nexSerial, "c0", cid=4)
    nexCheckbox1 = NexCheckbox(nexSerial, "c1", cid=5)
    nexCheckbox2 = NexCheckbox(nexSerial, "c2", cid=7)

    nexSerial.send("page pg_dsb_chk_rad")

    nexCheckbox0.value = False
    nexCheckbox1.value = False
    nexCheckbox2.value = False

    assert not nexCheckbox0.value

    time.sleep(1)

    nexCheckbox0.value = True

    assert nexCheckbox0.value

    time.sleep(1)

    nexCheckbox0.value = False

    assert not nexCheckbox0.value

    time.sleep(1)

    nexSerial.close()
