import time
from .events import (
    StringHeadEvent,
    NumberHeadEvent
)


try:
    import serial
    _HAS_PYSERIAL = True
except ImportError:
    _HAS_PYSERIAL = False


A_END_OF_CMD = [0xff, 0xff, 0xff]
S_END_OF_CMD = bytearray(A_END_OF_CMD)


def _format_cmd(cmd):
    return bytearray(cmd, encoding="ASCII") + S_END_OF_CMD


class AbstractSerialNex:
    def write(self, cmd):
        print(cmd)
        cmd = _format_cmd(cmd)
        return self.sp.write(cmd)

    def init(self):
        return

    def reset(self):
        cmd = "rest"
        return self.send(cmd)

    def read_all(self):
        return self.sp.read_all()

    def send(self, cmd):
        self.write(cmd)
        time.sleep(0.1)
        return self.read_all()

    def get_nex_string_command(self, cmd):
        return StringHeadEvent.parse(self.send(cmd)).value

    def set_nex_string_command(self, cmd):
        return self.send(cmd)

    def get_nex_number_command(self, cmd):
        return NumberHeadEvent.parse(self.send(cmd)).value

    def set_nex_number_command(self, cmd):
        return self.send(cmd)

    def get_nex_bool_command(self, cmd):
        return bool(NumberHeadEvent.parse(self.send(cmd)).value)

    def set_nex_bool_command(self, cmd):
        return self.send(cmd)

    @property
    def current_page(self):
        return self.get_nex_number_command("get page")

    def close(self):
        return self.sp.close()


if _HAS_PYSERIAL:
    class PySerialNex(AbstractSerialNex):
        def __init__(self, *args, **kwargs):
            self.sp = serial.Serial(*args, **kwargs)


class NexSerialMock(AbstractSerialNex):
    def __init__(self, *args, **kwargs):
        pass

    def write(self, cmd):
        pass

    def read(self):
        return None


"""
# PyBoard 1.1
# https://docs.micropython.org/en/latest/pyboard/pyboard/quickref.html
# RED: VIN
# BLACK: GND
# YELLOW: X9 (Board TX)
# BLUE: X10 (Board RX)

import machine
import time


class uPyNexSerial(AbstractSerialNex):
    def __init__(self, *args, **kwargs):
        self.sp = machine.UART(*args, **kwargs)

"""
