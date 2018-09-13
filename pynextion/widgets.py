from .objects import IWidget

from .interfaces import (
    NxInterface,
    IViewable,
    IBooleanValued,
    INumericalValued,
    IStringValued,
    IFontStyleable,
    IColourable,
    IPicturable,
    ITouchable,
    IWidthable,
    IHeightable
)


class NexButton(IWidget, IViewable, IStringValued, IFontStyleable, IColourable, ITouchable):
    pass


class NexCheckbox(IWidget, IViewable, IBooleanValued, IColourable, ITouchable):
    pass


class NexCrop(IWidget, IViewable, IPicturable, ITouchable):
    pass


class NexDualStateButton(IWidget, IViewable, IBooleanValued, IColourable, ITouchable):
    pass


class NexGauge(IWidget, IViewable, INumericalValued, IColourable, ITouchable):
    pass


class NexHotspot(IWidget, ITouchable):
    pass


class NexNumber(IWidget, IViewable, INumericalValued, IFontStyleable, IColourable, ITouchable):
    pass


class NexPage(IWidget):
    def show(self):
        # oid = self.nid.name
        oid = self._nid.pid
        return self._nid._nexserial.send("page %s" % oid)

    def ishown(self):
        pid1 = self.current_page
        pid2 = self.page
        return pid1 == pid2


class NexPicture(IWidget, IViewable, IPicturable):
    pass


class NexProgressBar(IWidget, IViewable, INumericalValued, IColourable, ITouchable):
    pass


class NexQRcode(IWidget, IViewable, IStringValued):
    pass


class NexRadio(IWidget, IViewable, IBooleanValued, IColourable, ITouchable):
    pass


class NexScrollText(IWidget, IViewable, IStringValued, IFontStyleable, IColourable, ITouchable):
    pass


class NexSliderCursor(IWidget, IWidthable, IHeightable):
    def __init__(self, nid):
        self._nid = nid


class NexSlider(IWidget, IViewable, INumericalValued, IColourable, ITouchable):
    @property
    def cursor(self):
        return NexSliderCursor(self._nid)


class NexText(IWidget, IViewable, IStringValued, IFontStyleable, IColourable, ITouchable):
    pass


class NexWaveformChannel:
    def __init__(self, nid, chid):
        self._nid = nid
        self._chid = chid  # channel id

    def append(self, value):
        nid = self._nid
        cid = nid.cid
        chid = self._chid
        nexserial = nid._nexserial
        if isinstance(value, list):
            vals = value
            n = len(vals)
            cmd = "addt %s,%s,%s" % (cid, chid, n)
            nexserial.send(cmd)
            nexserial.sp.write(bytearray(vals))
            return nexserial.read_all()
        else:
            if value < 0 or value > 255:
                raise(Exception("value must be in 0-255 range"))
            cmd = "add %s,%s,%s" % (cid, chid, value)
            return nexserial.send(cmd)


class NexWaveformChannels:
    def __init__(self, nid):
        self._nid = nid

    def __getitem__(self, id):
        return NexWaveformChannel(self._nid, id)


class NexWaveformGrid(IWidget, NxInterface):
    def __init__(self, nid):
        self._nid = nid

    @property
    def width(self):
        return self._get_nex_number_property("gdw")

    @width.setter
    def width(self, value):
        self._set_nex_number_property("gdw", value)

    @property
    def height(self):
        return self._get_nex_number_property("gdh")

    @height.setter
    def height(self, value):
        self._set_nex_number_property("gdh", value)

    @property
    def color(self):
        return self._get_nex_number_property("gdc")

    @color.setter
    def color(self, value):
        self._set_nex_number_property("gdc", value)


class NexWaveform(IWidget, IViewable, IColourable, ITouchable):
    @property
    def grid(self):
        return NexWaveformGrid(self._nid)

    @property
    def channels(self):
        return NexWaveformChannels(self._nid)
