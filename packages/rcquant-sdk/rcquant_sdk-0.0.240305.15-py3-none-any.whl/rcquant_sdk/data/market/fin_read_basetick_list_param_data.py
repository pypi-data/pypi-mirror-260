from typing import List
from ...interface import IData
from .basetick_data import BaseTickData
from ...packer.market.fin_read_basetick_list_param_data_packer import FinReadBaseTickListParamDataPacker


class FinReadBaseTickListParamData(IData):
    def __init__(self, exchange_id: str = '', instrument_id: str = '', base_path: str = '', start_date: int = 0, end_date: int = 99999999, tick_list: List[BaseTickData] = [], is_return_list: bool = False):
        super().__init__(FinReadBaseTickListParamDataPacker(self))
        self._ExchangeID: str = exchange_id
        self._InstrumentID: str = instrument_id
        self._BasePath: str = base_path
        self._StartDate: int = start_date
        self._EndDate: int = end_date
        self._TickList: list = tick_list
        self._IsReturnList: bool = is_return_list

    @property
    def ExchangeID(self):
        return self._ExchangeID

    @ExchangeID.setter
    def ExchangeID(self, value: str):
        self._ExchangeID = value

    @property
    def InstrumentID(self):
        return self._InstrumentID

    @InstrumentID.setter
    def InstrumentID(self, value: str):
        self._InstrumentID = value

    @property
    def BasePath(self):
        return self._BasePath

    @BasePath.setter
    def BasePath(self, value: str):
        self._BasePath = value

    @property
    def StartDate(self):
        return self._StartDate

    @StartDate.setter
    def StartDate(self, value: int):
        self._StartDate = value

    @property
    def EndDate(self):
        return self._EndDate

    @EndDate.setter
    def EndDate(self, value: int):
        self._EndDate = value

    @property
    def TickList(self):
        return self._TickList

    @TickList.setter
    def TickList(self, value: List[BaseTickData]):
        self._TickList = value

    @property
    def IsReturnList(self):
        return self._IsReturnList

    @IsReturnList.setter
    def IsReturnList(self, value: bool):
        self._IsReturnList = value
