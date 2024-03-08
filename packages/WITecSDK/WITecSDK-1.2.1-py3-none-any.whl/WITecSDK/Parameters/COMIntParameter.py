from WITecSDK.Parameters.COMParameterBase import COMSingleValueParameter, ValueOutOfRangeException
from WITecSDK import COMClient, IBUCSInt, IBUCSIntMinMaxValues, IBUCSSingleValueHasLimits

class COMIntParameter(COMSingleValueParameter):
    
    def __init__(self, aParameterName: str, aCOMClient: COMClient):
        super().__init__(aCOMClient, aParameterName)
        self.modifier = self._castToInterface(self.modifier, IBUCSInt)
        self.rangevals = self._castToInterface(self.modifier, IBUCSIntMinMaxValues)
        self.hasLimits = self._castToInterface(self.modifier, IBUCSSingleValueHasLimits)
        self.limits = self.HasLimits()

    def GetValue(self) -> int:
        return self.modifier.GetValue()

    def SetValue(self, aValue: int):
        range = self.GetRange()
        if self.limits[0] and range[0] > aValue:
            raise ValueOutOfRangeException(f'Value is smaller than {self.range[0]}')
        if self.limits[1] and range[1] < aValue:
            raise ValueOutOfRangeException(f'Value is bigger than {self.range[1]}')
        self._throwExceptionIfNoWriteAccess()
        self.modifier.SetValue(aValue)

    def GetRange(self) -> tuple[int, int]:
        minval = self.rangevals.GetMinimum()
        maxval = self.rangevals.GetMaximum()
        return minval, maxval
    
    def HasLimits(self) -> tuple[bool, bool]:
        minlim = self.hasLimits.HasMinimum()
        maxlim = self.hasLimits.HasMaximum()
        return minlim, maxlim

    def __del__(self):
        self._releaseSubSystem(self.rangevals)
        self._releaseSubSystem(self.hasLimits)
        super().__del__()