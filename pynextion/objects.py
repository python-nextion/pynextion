PID_DEFAULT = 0
CID_DEFAULT = 0


class NexId:
    def __init__(self, nexserial, name, pid, cid):
        self._nexserial = nexserial  # serial port
        self.name = name
        self.pid = pid
        self.cid = cid


class IWidget:
    def __init__(self, nexserial, name, pid=PID_DEFAULT, cid=CID_DEFAULT):
        self._nid = NexId(nexserial, name, pid, cid)

    @property
    def pid(self):
        return self._nid.pid

    @property
    def cid(self):
        return self._nid.cid

    @property
    def name(self):
        return self._nid.name
