from pynextion.enhanced import GPIO


def test_enhanced_gpio():
    assert GPIO.Mode.PULL_UP_INPUT_MODE.value == 0x00


"""
def test_enhanced_eeprom():
     assert ...


def test_enhanced_rtc():
     assert ...
"""
