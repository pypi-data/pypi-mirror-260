from WITecSDK.Parameters import COMParameters

class TrueSurface:

    _parampath = "MultiComm|MicroscopeControl|TrueSurface|"

    def __init__(self, aCOMParameters: COMParameters):
        self._trueSurfaceStateCOM = aCOMParameters.GetEnumParameter(self._parampath + "State")

    @property
    def State(self) -> int:
        return self._trueSurfaceStateCOM.GetValue()
    
    def GetStates(self) -> dict:
        return self._trueSurfaceStateCOM.GetAvailableValues()

    def setRunning(self):
        self._trueSurfaceStateCOM.SetValue(2)

    def setPrepare(self):
        self._trueSurfaceStateCOM.SetValue(1)

    def setOff(self):
        self._trueSurfaceStateCOM.SetValue(0)


class TrueSurface62(TrueSurface):

    def __init__(self, aCOMParameters: COMParameters):
        super().__init__(aCOMParameters)
        self._focusShiftCOM = aCOMParameters.GetFloatParameter(self._parampath + "FocusShift")
        self._minValueCOM = aCOMParameters.GetFloatParameter(self._parampath + "MinValue")
        self._pGainCOM = aCOMParameters.GetFloatParameter(self._parampath + "PGain")
        self._iGainCOM = aCOMParameters.GetFloatParameter(self._parampath + "IGain")
        self._laserIntensityCOM = aCOMParameters.GetIntParameter(self._parampath + "LaserIntensity")
        self._detectorGainCOM = aCOMParameters.GetEnumParameter(self._parampath + "DetectorGain")
        self._useAutomaticGainCOM = aCOMParameters.GetBoolParameter(self._parampath + "UseAutomaticGain")

    @property
    def FocusShift(self) -> float:
        return self._focusShiftCOM.GetValue()
    
    @property
    def MinValue(self) -> float:
        return self._minValueCOM.GetValue()
    
    @property
    def PGain(self) -> float:
        return self._pGainCOM.GetValue()
    
    @property
    def IGain(self) -> float:
        return self._iGainCOM.GetValue()
    
    @property
    def LaserIntensity(self) -> int:
        return self._laserIntensityCOM.GetValue()
        
    @property
    def DetectorGain(self) -> int:
        return self._detectorGainCOM.GetValue()
    
    def GetDetectorGains(self) -> dict:
        return self._detectorGainCOM.GetAvailableValues()
    
    @property
    def UseAutomaticGain(self) -> bool:
        return self._useAutomaticGainCOM.GetValue()
    

# TrueSurface|DetectorGain  <enum>
#    Get the Detector Gain - Enum Values: 0: Low, 1: Medium, 2: High, 3: Maximum
#    This parameter is read only.
