from WITecSDK.Parameters import COMParameters

class Spectrograph:

    def __init__(self, aCOMParameters: COMParameters, specNo: int):
        parampath = "UserParameters|Spectrograph" + str(specNo)
        self._gratingCOM = aCOMParameters.GetEnumParameter(parampath + "|Grating")
        self._centerWavelengthCOM = aCOMParameters.GetFloatParameter(parampath + "|CenterWavelength")
        self._spectralCenterCOM = aCOMParameters.GetFloatParameter(parampath + "|SpectralCenter")
        self._spectralUnitCOM = aCOMParameters.GetEnumParameter(parampath + "|SpectralUnit")

    @property
    def CenterWavelength(self) -> float:
        return self._centerWavelengthCOM.GetValue()

    @CenterWavelength.setter
    def CenterWavelength(self, centerWavelength: float):
        self._centerWavelengthCOM.SetValue(centerWavelength)

    @property
    def SpectralCenter(self) -> float:
        return self._spectralCenterCOM.GetValue()

    @SpectralCenter.setter
    def SpectralCenter(self, spectralCenter: float):
        self._spectralCenterCOM.SetValue(spectralCenter)

    @property
    def Grating(self) -> int:
        return self._gratingCOM.GetValue()

    @Grating.setter
    def Grating(self, grating: int):
        self._gratingCOM.SetValue(grating)

    def GetGratings(self) -> dict:
        return self._gratingCOM.GetAvailableValues()
    
    @property
    def Unit(self) -> int:
        return self._spectralUnitCOM.GetValue()

    @Unit.setter
    def Unit(self, unit: int):
        self._spectralUnitCOM.SetValue(unit)

    def GetUnits(self) -> dict:
        return self._spectralUnitCOM.GetAvailableValues()