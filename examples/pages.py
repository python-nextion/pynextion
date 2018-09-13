import pytest
from .config import PORT_DEFAULT
import time
from pynextion import PySerialNex
from pynextion.widgets import NexPage


@pytest.mark.parametrize("port", [PORT_DEFAULT])
def test_pages(port):
    nexserial = PySerialNex(port)
    nexpages = []
    pages_nb = 22
    for i in range(pages_nb):
        print(i)
        page = NexPage(nexserial, "page%d" % i, i)
        nexpages.append(page)

    for page in nexpages:
        print(page.show())
        time.sleep(0.5)

    page = nexpages[0]
    page.show()

    time.sleep(2)

    assert nexserial.current_page == page.pid

    assert nexpages[0].ishown()
    assert not nexpages[1].ishown()

    nexserial.close()
