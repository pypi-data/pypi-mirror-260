from ...interface import IPacker


class FinReadOHLCListParamDataPacker(IPacker):
    def __init__(self, obj) -> None:
        super().__init__(obj)

    def obj_to_tuple(self):
        return [str(self._obj.InstrumentID), str(self._obj.Range),
                int(self._obj.StartDate), int(self._obj.EndDate),
                str(self._obj.BasePath), list(self._obj.OHLCList)]

    def tuple_to_obj(self, t):
        if len(t) >= 6:
            self._obj.InstrumentID = t[0]
            self._obj.Range = t[1]
            self._obj.StartDate = t[2]
            self._obj.EndDate = t[3]
            self._obj.BasePath = t[4]
            self._obj.OHLCList = t[5]

            return True
        return False
