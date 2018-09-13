import pytest
from pynextion.resources import Picture, Font


def test_resource_picture():
    pic = Picture(1)
    assert pic.id == 1
    with pytest.raises(Exception):
        Picture(256)


def test_resource_font():
    font = Font(1)
    assert font.id == 1
    with pytest.raises(Exception):
        Font(256)
