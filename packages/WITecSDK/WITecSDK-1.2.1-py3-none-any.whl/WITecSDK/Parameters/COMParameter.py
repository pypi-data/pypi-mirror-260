from WITecSDK.Parameters.COMParameterBase import COMParameterBase, COMSingleValueParameter
from WITecSDK import COMClient, IBUCSBool, IBUCSString, IBUCSTrigger

class COMBoolParameter(COMSingleValueParameter):

    def __init__(self, aParameterName: str, aCOMClient: COMClient):
        super().__init__(aCOMClient, aParameterName)
        self.modifier = self._castToInterface(self.modifier, IBUCSBool)

    def GetValue(self) -> bool:
        return self.modifier.GetValue()

    def SetValue(self, aValue: bool):
        self._throwExceptionIfNoWriteAccess()
        self.modifier.SetValue(aValue)


class COMStringParameter(COMSingleValueParameter):
    
    def __init__(self, aParameterName: str, aCOMClient: COMClient):
        super().__init__(aCOMClient, aParameterName)
        self.modifier = self._castToInterface(self.modifier, IBUCSString)

    def GetValue(self) -> str:
        return self.modifier.GetValue()

    def SetValue(self, aValue: str):
        self._throwExceptionIfNoWriteAccess()
        self.modifier.SetValue(aValue)


class COMTriggerParameter(COMParameterBase):

    def __init__(self, aParameterName: str, aCOMClient: COMClient):
        super().__init__(aCOMClient, aParameterName)
        self.modifier = self._castToInterface(self.modifier, IBUCSTrigger)

    def ExecuteTrigger(self):
        self._throwExceptionIfNoWriteAccess()
        self.modifier.OperateTrigger()