from WITecSDK.Parameters import COMParameters
from WITecSDK.Modules.BeamPath import AutomatedCoupler

class Illumination:

    _parampath = "MultiComm|MicroscopeControl|WhiteLight|"

    def __init__(self, aCOMParameters: COMParameters, illuType: str):
        parampath = self._parampath + illuType
        self._illuminationOnCOM = aCOMParameters.GetBoolParameter(parampath + "|On")
        self._brightnessPercentageCOM = aCOMParameters.GetFloatParameter(parampath + "|BrightnessPercentage")

    @property
    def SwitchedOn(self) -> bool:
        return self._illuminationOnCOM.GetValue()

    @SwitchedOn.setter
    def SwitchedOn(self, isOn: bool):
        self._illuminationOnCOM.SetValue(isOn)

    @property
    def BrightnessPercentage(self) -> float:
        return self._brightnessPercentageCOM.GetValue()

    @BrightnessPercentage.setter
    def BrightnessPercentage(self, spectralCenter: float):
        self._brightnessPercentageCOM.SetValue(spectralCenter)

class TopIllumination(Illumination):

    def __init__(self, aCOMParameters: COMParameters):
        super().__init__(aCOMParameters, "Top")
        self.WhiteLightCoupler = AutomatedCoupler(aCOMParameters, self._parampath + "WhiteLightCoupler")

class BottomIllumination(Illumination):

    def __init__(self, aCOMParameters: COMParameters):
        super().__init__(aCOMParameters, "Bottom")