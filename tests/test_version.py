import pynextion


def test_version():
    assert isinstance(pynextion.__version__, str)
