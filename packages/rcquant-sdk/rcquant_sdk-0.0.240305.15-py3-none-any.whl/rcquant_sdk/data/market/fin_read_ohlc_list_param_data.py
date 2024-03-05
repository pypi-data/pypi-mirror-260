from typing import List
from ...interface import IData
from .ohlc_data import OHLCData
from ...packer.market.fin_read_ohlc_list_param_data_packer import FinReadOHLCListParamDataPacker


class FinReadOHLCListParamData(IData):
    def __init__(self, instrument_id: str = '', range: str = '', start_date: int = 0, end_date: int = 99999999, base_path: str = '', ohlc_list: list = '', is_return_list: bool = False):
        super().__init__(FinReadOHLCListParamDataPacker(self))
        self._Range: str = range
        self._InstrumentID: str = instrument_id
        self._StartDate: int = start_date
        self._EndDate: int = end_date
        self._BasePath: str = base_path
        self._OHLCList: list = ohlc_list
        self._IsReturnList: bool = is_return_list

    @property
    def Range(self):
        return self._Range

    @Range.setter
    def Range(self, value: str):
        self._Range = value

    @property
    def InstrumentID(self):
        return self._InstrumentID

    @InstrumentID.setter
    def InstrumentID(self, value: str):
        self._InstrumentID = value

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
    def BasePath(self):
        return self._BasePath

    @BasePath.setter
    def BasePath(self, value: str):
        self._BasePath = value

    @property
    def OHLCList(self):
        return self._OHLCList

    @OHLCList.setter
    def OHLCList(self, value: List[OHLCData]):
        self._OHLCList = value

    @property
    def IsReturnList(self):
        return self._IsReturnList

    @IsReturnList.setter
    def IsReturnList(self, value: bool):
        self._IsReturnList = value
