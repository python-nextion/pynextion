import pytest
from .config import PORT_DEFAULT
import time
from pynextion import PySerialNex
from pynextion.widgets import NexPicture
from pynextion.resources import Picture


@pytest.mark.parametrize("port", [PORT_DEFAULT])
def test_NexPicture(port):
    nexSerial = PySerialNex(port)

    nexPicture = NexPicture(nexSerial, "p0", cid=1)

    nexSerial.send("page pg_pic")

    for i in range(1, 5):
        time.sleep(1)
        # nexPicture.picture = i
        nexPicture.picture = Picture(i)
        # assert nexPicture.picture == Picture(i)  # ToDo

    nexSerial.close()
