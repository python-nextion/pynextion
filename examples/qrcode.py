import pytest
from .config import PORT_DEFAULT
import time
from pynextion import PySerialNex
from pynextion.widgets import NexQRcode, NexText


@pytest.mark.parametrize("port", [PORT_DEFAULT])
def test_NexQRCode(port):
    nexSerial = PySerialNex(port)

    nexQRcode = NexQRcode(nexSerial, "qr0", cid=1)
    nexText = NexText(nexSerial, "t1", cid=3)

    nexSerial.send("page pg_qr")

    time.sleep(1)

    text = "Hello"
    nexQRcode.text = text
    nexText.text = text

    time.sleep(2)

    # text = "https://github.com/scls19fr/pynextion"
    text = "http://bit.ly/2vWS75r"
    nexText.text = text
    # nexQRcode.textmaxlength = len(text)
    # nexQRcode.textmaxlength = 50
    # time.sleep(1)
    nexQRcode.text = text

    assert nexText.text == text
    assert nexQRcode.text == text

    nexSerial.close()
