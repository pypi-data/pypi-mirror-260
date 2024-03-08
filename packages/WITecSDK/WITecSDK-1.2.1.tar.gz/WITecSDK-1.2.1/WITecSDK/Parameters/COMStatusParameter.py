from WITecSDK.Parameters.COMParameterBase import COMParameterBase
from WITecSDK import COMClient, IBUCSStatusContainer

class COMStatusParameter(COMParameterBase):

    def __init__(self, aParameterName: str, aCOMClient: COMClient):
        super().__init__(aCOMClient, aParameterName)
        self.modifier = self._castToInterface(self.modifier, IBUCSStatusContainer)

    def Update(self):
        self.modifier.Update()

    def GetStatusProperties(self) -> tuple[str, str]:
        self.Update()
        caption, unit, res = self._reorder(self.modifier.GetStatusProperties())
        self._throwExceptionIfNotSuccessful(res)
        return caption, unit
    
    def _throwExceptionIfNotSuccessful(self, aRes: bool):
        if not aRes:
            raise Exception('Reading status parameter ' + self.GetName() + ' was not successful. Result: ' + str(aRes))

class COMStringStatusParameter(COMStatusParameter):

    def GetValue(self) -> str:
        self.Update()
        aStringValue, res = self._reorder(self.modifier.GetSingleValueAsString())
        self._throwExceptionIfNotSuccessful(res)
        return aStringValue

class COMIntStatusParameter(COMStatusParameter):

    def GetValue(self) -> int:
        self.Update()
        aIntValue, res = self._reorder(self.modifier.GetSingleValueAsInt())
        self._throwExceptionIfNotSuccessful(res)
        return aIntValue

class COMFloatStatusParameter(COMStatusParameter):
    
    def GetValue(self) -> float:
        self.Update()
        aFloatValue, res = self._reorder(self.modifier.GetSingleValueAsDouble())
        self._throwExceptionIfNotSuccessful(res)
        return aFloatValue

class COMBoolStatusParameter(COMIntStatusParameter):
    
    def GetValue(self) -> bool:
        return super().GetValue() != 0

class COMArrayStatusParameter(COMStatusParameter):
    
    def GetValue(self):
        self.Update()
        dims, dimsext, vals, res = self._reorder(self.modifier.GetStatusArray())
        self._throwExceptionIfNotSuccessful(res)
        return dims, dimsext, vals
