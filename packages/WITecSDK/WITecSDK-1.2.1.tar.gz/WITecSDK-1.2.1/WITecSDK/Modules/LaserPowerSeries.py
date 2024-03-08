from WITecSDK.Parameters import COMParameters
from WITecSDK.Modules.SlowTimeSeriesBase import SlowSeriesBase

class LaserPowerSeries(SlowSeriesBase):

    def __init__(self, aCOMParameters: COMParameters):
        super().__init__(aCOMParameters)
        self._parampath = self._parampath + "LaserPowerSeries|"
        self._startLaserPowerSeriesCOM = aCOMParameters.GetTriggerParameter(self._parampath + "StartLaserPowerSeries")
        self._numberOfLasersCOM = aCOMParameters.GetIntParameter(self._parampath + "NumberOfLaserPowerValues")
        self._startLaserPowerCOM = aCOMParameters.GetFloatParameter(self._parampath + "StartLaserPower")
        self._stopLaserPowerCOM = aCOMParameters.GetFloatParameter(self._parampath + "StopLaserPower")
        self._forwardAndBackwardCOM = aCOMParameters.GetBoolParameter(self._parampath + "ForwardAndBackward")
        self._keepDoseConstantCOM = aCOMParameters.GetBoolParameter(self._parampath + "KeepDoseConstant")

    @property
    def NumberOfValues(self) -> int:
        return self._numberOfLasersCOM.GetValue()

    @NumberOfValues.setter
    def NumberOfValues(self, numval: int):
        self._numberOfLasersCOM.SetValue(numval)
        
    def Start(self):
        self._startLaserPowerSeriesCOM.ExecuteTrigger()

    @property
    def StartLaserPower(self) -> float:
        return self._startLaserPowerCOM.GetValue()

    @StartLaserPower.setter
    def StartLaserPower(self, laserPower: float):
        self._startLaserPowerCOM.SetValue(laserPower)

    @property
    def StopLaserPower(self) -> float:
        return self._stopLaserPowerCOM.GetValue()

    @StopLaserPower.setter
    def StopLaserPower(self, laserPower: float):
        self._stopLaserPowerCOM.SetValue(laserPower)