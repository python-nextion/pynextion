class NexResource:
    @classmethod
    def _assert_uint8(cls, value):
        if value < 0 or value > 255:
            raise(Exception("Value must be in 0-255 range"))


class Picture(NexResource):
    def __init__(self, id):
        self._assert_uint8(id)
        self.id = id


class Font(NexResource):
    def __init__(self, id):
        self._assert_uint8(id)
        self.id = id


FONT_DEFAULT = Font(0)
