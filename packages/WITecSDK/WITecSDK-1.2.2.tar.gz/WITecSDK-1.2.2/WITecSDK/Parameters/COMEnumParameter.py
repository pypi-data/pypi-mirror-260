from WITecSDK.Parameters.COMParameterBase import COMSingleValueParameter
from WITecSDK import COMClient, IBUCSEnum

class COMEnumParameter(COMSingleValueParameter):

    def __init__(self, aParameterName: str, aCOMClient: COMClient):
        super().__init__(aCOMClient, aParameterName)
        self.modifier = self._castToInterface(self.modifier, IBUCSEnum)
                
    def SetValue(self, aEnumIndex: int):
        self._throwExceptionIfNoWriteAccess()
        self.modifier.SetValueNumeric(aEnumIndex)

    def GetEnumValue(self) -> tuple[str, int]:
        value = self._reorder(self.modifier.GetValue())
        return value
    
    def GetValue(self) -> int:
        value = self.GetEnumValue()
        return value[1]
    
    def GetStringValue(self) -> str:
        value = self.GetEnumValue()
        return value[0]

    def GetAvailableValues(self) -> dict[int, str] | None:
        index, strings, numValues = self._reorder(self.modifier.GetAvailableValues())
        
        if index is None or strings is None:
            return None

        enumValues = {}
        for i in range(numValues):
            enumValues[index[i]] = strings[i]

        return enumValues
