import wx
import wx.lib.agw.pybusyinfo as PBI
BusyInfo = PBI.PyBusyInfo


class BusyFrame:
    @property
    def busy(self):
        try:
            _busy_flag = self._busy
            return _busy_flag
        except AttributeError:
            self._busy = False
            return self._busy

    @busy.setter
    def busy(self, value):
        if value:
            self._busy = True
            self._disableAll = wx.WindowDisabler()
            if not isinstance(value, str):
                v = _("Busy...")
            else:
                v = value
            self._wait = BusyInfo("Please wait. \n%s" % v, parent=self)
            wx.GetApp().Yield()
        else:
            self._busy = False
            self._wait = None
            self._disableAll = None
            wx.GetApp().Yield()

