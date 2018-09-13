from pynextion.events import (
    Event,
    TouchEvent,
    CurrentPageIDHeadEvent,
    PositionHeadEvent,
    SleepPositionHeadEvent,
    StringHeadEvent,
    NumberHeadEvent
)
from pynextion.constants import Return


def test_event_touch_constants():
    assert Event.Touch.Press.value == 0x01


def test_event_touchevent():
    msg = [0x65, 0x00, 0x02, 0x01, 0xff, 0xff, 0xff]
    evt = TouchEvent.parse(msg)
    assert evt.code == Return.Code.EVENT_TOUCH_HEAD
    assert evt.pid == 0x00
    assert evt.cid == 0x02
    assert evt.tevts == Event.Touch.Press  # touch event state


def test_CurrentPageIDHeadEvent():
    msg = [0x66, 0x02, 0xff, 0xff, 0xff]
    evt = CurrentPageIDHeadEvent.parse(msg)
    assert evt.code == Return.Code.CURRENT_PAGE_ID_HEAD
    assert evt.pid == 0x02


def test_PositionHeadEvent():
    msg = [0x67, 0x00, 0x7a, 0x00, 0x1e, 0x01, 0xff, 0xff, 0xff]
    evt = PositionHeadEvent.parse(msg)
    assert evt.code == Return.Code.EVENT_POSITION_HEAD
    assert evt.x == 122
    assert evt.y == 30
    assert evt.tevts == Event.Touch.Press


def test_SleepPositionHeadEvent():
    msg = [0x68, 0x00, 0x7a, 0x00, 0x1e, 0x01, 0xff, 0xff, 0xff]
    evt = SleepPositionHeadEvent.parse(msg)
    assert evt.code == Return.Code.EVENT_SLEEP_POSITION_HEAD
    assert evt.x == 122
    assert evt.y == 30
    assert evt.tevts == Event.Touch.Press


def test_StringHeadEvent():
    msg = [0x70, 0x61, 0x62, 0x63, 0xff, 0xff, 0xff]
    evt = StringHeadEvent.parse(msg)
    assert evt.code == Return.Code.STRING_HEAD
    assert evt.value == "abc"


def test_NumberHeadEvent():
    msg = [0x71, 0x66, 0x00, 0x00, 0x00, 0xff, 0xff, 0xff]
    evt = NumberHeadEvent.parse(msg)
    assert evt.code == Return.Code.NUMBER_HEAD
    assert evt.value == 102

    msg = [0x71, 0x66, 0x01, 0x00, 0x00, 0xff, 0xff, 0xff]
    evt = NumberHeadEvent.parse(msg)
    assert evt.value == 0x00000166  # 102 + 256

    msg = [0x71, 0x01, 0xff, 0x00, 0x00, 0xff, 0xff, 0xff]
    evt = NumberHeadEvent.parse(msg)
    assert evt.value == 0x0000ff01  # 65281

    msg = [0x71, 0x01, 0x00, 0xff, 0x00, 0xff, 0xff, 0xff]
    evt = NumberHeadEvent.parse(msg)
    assert evt.value == 0x00ff0001  # 16711681

    msg = [0x71, 0x01, 0x00, 0x00, 0xff, 0xff, 0xff, 0xff]
    evt = NumberHeadEvent.parse(msg)
    assert evt.value == 0xff000001

    msg = [0x71, 0xff, 0xff, 0xff, 0x7f, 0xff, 0xff, 0xff]
    evt = NumberHeadEvent.parse(msg)
    # assert evt.value == typemax(Int32)  # ToDo

    msg = [0x71, 0xfe, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
    evt = NumberHeadEvent.parse(msg)
    assert evt.value == 0xfffffffe
    assert evt.signed_value == -2

    msg = [0x71, 0x00, 0x00, 0x00, 0x80, 0xff, 0xff, 0xff]
    evt = NumberHeadEvent.parse(msg)
    assert evt.value == 0x80000000
    # assert evt.signed_value == typemin(Int32)  # ToDo
