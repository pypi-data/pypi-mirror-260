from WITecSDK import COMClient, IBUCSSubSystemInfo, IBUCSSingleValue

class COMParameterBase:

    def __init__(self, aCOMClient: COMClient, aParameterName: str):
        self._comClient = aCOMClient
        self.modifier = self._getDefaultInterface(aParameterName)
        self.subsysinfo = self._castToInterface(self.modifier, IBUCSSubSystemInfo)

    def GetName(self) -> str:
        return self.subsysinfo.GetName()

    def GetEnabled(self) -> bool:
        return self.subsysinfo.GetEnabled()

    def _getDefaultInterface(self, aParameterName: str):
        try:
            return self._comClient.GetSubSystemDefaultInterface(aParameterName)
        except Exception as e:
            raise ParameterNotAvailableException("Parameter Not Available: " + aParameterName) from e
    
    def _releaseSubSystem(self, subSystem):
        self._comClient.ReleaseSubSystemInterface(subSystem)

    def _castToInterface(self, aObj, aInterface):
        return self._comClient.CastToInterface(aObj, aInterface)
    
    def _reorder(self, aValues: tuple) -> tuple:
        return self._comClient.Reorder(aValues)

    def _convertToBSTRArray(self, datalist: list[str]):
        return self._comClient.ConvertToBSTRArray(datalist)

    def _convertToFloatArray(self, datalist: list[float]):
        return self._comClient.ConvertToFloatArray(datalist)
    
    def _throwExceptionIfDisabled(self):
        if not self.GetEnabled():
            raise ParameterDisabledException('Parameter ' + self.GetName() + ' is disabled.')
        
    def _throwExceptionIfNoWriteAccess(self):
        self._throwExceptionIfDisabled()
        if not self._comClient.WriteAccess:
            raise NoWriteAccessException('No write access granted to perform an action on parameter ' + self.GetName() + '.')
    
    def __del__(self):
        self._releaseSubSystem(self.modifier)
        self._releaseSubSystem(self.subsysinfo)


class COMSingleValueParameter(COMParameterBase):

    def __init__(self, aCOMClient: COMClient, aParameterName: str):
        super().__init__(aCOMClient, aParameterName)
        self.singleval = self._castToInterface(self.modifier, IBUCSSingleValue)

    def GetDisplayName(self) -> str:
        return self.singleval.GetDisplayName()

    def __del__(self):
        self._releaseSubSystem(self.singleval)
        super().__del__()

class ValueOutOfRangeException(Exception):
    pass

class ParameterNotAvailableException(Exception):
    pass

class NoWriteAccessException(Exception):
    pass

class ParameterDisabledException(Exception):
    pass