from WITecSDK.Parameters import COMParameters
from asyncio import sleep

class Heating:

    def __init__(self, aCOMParameters: COMParameters):
        parampath = "UserParameters|Heating|"
        self._enabledCOM = aCOMParameters.GetBoolParameter(parampath + "Enabled")
        self._setpointCOM = aCOMParameters.GetFloatParameter(parampath + "Setpoint")
        self._rampEndCOM = aCOMParameters.GetFloatParameter(parampath + "TemperatureRamp|RampEnd")
        self._gradientCOM = aCOMParameters.GetFloatParameter(parampath + "TemperatureRamp|Gradient")
        self._startGradientCOM = aCOMParameters.GetTriggerParameter(parampath + "TemperatureRamp|StartGradient")
        self._stopGradientCOM = aCOMParameters.GetTriggerParameter(parampath + "TemperatureRamp|StopGradient")
        self._currentTempCOM = aCOMParameters.GetFloatParameter("Status|Hardware|Controller|DataChannels|HeatingStageTemperature")

    def Initialize(self, gradient: float, tempSetpoint: float):
        self.Gradient = gradient
        self.TemperatureSetpoint = tempSetpoint
        self.Enabled = True

    @property
    def Gradient(self) -> float:
        return self._gradientCOM.GetValue()

    @Gradient.setter
    def Gradient(self, gradient: float):
        self._gradientCOM.SetValue(gradient)
    
    @property
    def TemperatureSetpoint(self) -> float:
        return self._rampEndCOM.GetValue()

    @TemperatureSetpoint.setter
    def TemperatureSetpoint(self, tempSetpoint: float):
        self._rampEndCOM.SetValue(tempSetpoint)

    @property
    def CurrentSetpoint(self) -> float:
        return self._setpointCOM.GetValue()

    @CurrentSetpoint.setter
    def CurrentSetpoint(self, setpointTemp: float):
        self._setpointCOM.SetValue(setpointTemp)

    @property
    def Enabled(self) -> bool:
        return self._enabledCOM.GetValue()
    
    @Enabled.setter
    def Enabled(self, value):
        self._enabledCOM.SetValue(value)

    @property
    def CurrentTemperature(self) -> float:
        return self._currentTempCOM.GetValue()

    def StartGradient(self):
        self._startGradientCOM.ExecuteTrigger()

    def StopGradient(self):
        self._stopGradientCOM.ExecuteTrigger()