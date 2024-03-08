from WITecSDK.Parameters.COMStatusParameter import COMStatusParameter
from WITecSDK import COMClient, IBUCSFillStatus

class COMFillStatusParameter(COMStatusParameter):

    def __init__(self, aParameterName: str, aCOMClient: COMClient):
        super().__init__(aParameterName, aCOMClient)
        self.fillvals = self._castToInterface(self.modifier, IBUCSFillStatus)

    def fillDataArray(self, dataarray):
        self._throwExceptionIfNoWriteAccess()
        self.fillvals.FillDataArray(dataarray)

    def __del__(self):
        self._releaseSubSystem(self.fillvals)
        super().__del__()

class COMStringFillStatusParameter(COMFillStatusParameter):

    def WriteArray(self, datalist: list[str]):
        isstr = [isinstance(x,str) for x in datalist]
        if not False in isstr:
            self.fillDataArray(self._convertToBSTRArray(datalist))
        else:
            raise Exception("Non-matching datatypes for IBUCSFillStatus")
        
class COMFloatFillStatusParameter(COMFillStatusParameter):

    def WriteArray(self, datalist: list[float]):
        isnum = [isinstance(x,(int,float)) for x in datalist]
        if not False in isnum:
            self.fillDataArray(self._convertToFloatArray(datalist))
        else:
            raise Exception("Non-matching datatypes for IBUCSFillStatus")
