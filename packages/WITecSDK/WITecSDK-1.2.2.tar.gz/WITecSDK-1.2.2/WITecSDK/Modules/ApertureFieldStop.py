from WITecSDK.Parameters import COMParameters

class ApertureFieldStop:

    def __init__(self, aCOMParameters: COMParameters):
        parampath = "MultiComm|MicroscopeControl|OpticControl|"
        self._fieldStopCOM = aCOMParameters.GetFloatParameter(parampath + "FieldStop")
        self._apertureStopCOM = aCOMParameters.GetFloatParameter(parampath + "ApertureStop")

    @property
    def FieldStop(self) -> float:
        return self._fieldStopCOM.GetValue()

    @FieldStop.setter
    def FieldStop(self, value: float):
        self._fieldStopCOM.SetValue(value)

    @property
    def ApertureStop(self) -> float:
        return self._apertureStopCOM.GetValue()

    @ApertureStop.setter
    def ApertureStop(self, value: float):
        self._apertureStopCOM.SetValue(value)