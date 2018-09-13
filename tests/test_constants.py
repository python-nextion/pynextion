import pytest
from pynextion.constants import (
    Return,
    Alignment,
    Background,
    Colour,
    Scroll,
    Format,
    Baudrate
)


def test_constants_return_code():
    assert Return.Code.CMD_FINISHED.value == 0x01
    assert Return.Code(0x01) == Return.Code.CMD_FINISHED


def test_constants_return_mode():
    assert Return.Mode.ALWAYS.value == 0x03


def test_constants_alignement():
    assert Alignment.Horizontal.CENTRE.value == 1
    assert Alignment.Vertical.CENTRE.value == 1


def test_constants_background():
    assert Background.IMAGE.value == 2


def test_constants_colour():
    assert Colour.RED.value == 63488


def test_constants_scroll():
    assert Scroll.Direction.RIGHT_TO_LEFT.value == 1


def test_constants_format():
    assert Format.DECIMAL.value == 0


def test_constants_baudrate():
    assert 9600 in Baudrate.SUPPORTED
    assert Baudrate.at(9600) == 9600
    with pytest.raises(Exception):
        Baudrate.at(123)
