from ...interface import IPacker


class FinReadBaseTickListParamDataPacker(IPacker):
    def __init__(self, obj) -> None:
        super().__init__(obj)

    def obj_to_tuple(self):
        return [str(self._obj.ExchangeID), str(self._obj.InstrumentID), str(self._obj.BasePath), int(self._obj.StartDate),
                int(self._obj.EndDate), list(self._obj.TickList)]

    def tuple_to_obj(self, t):
        if len(t) >= 6:
            self._obj.ExchangeID = t[0]
            self._obj.InstrumentID = t[1]
            self._obj.BasePath = t[2]
            self._obj.StartDate = t[3]
            self._obj.EndDate = t[4]
            self._obj.TickList = t[5]

            return True
        return False
