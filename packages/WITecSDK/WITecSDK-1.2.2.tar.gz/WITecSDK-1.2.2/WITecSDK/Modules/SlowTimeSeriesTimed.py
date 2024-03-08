from WITecSDK.Parameters import COMParameters
from WITecSDK.Modules.SlowTimeSeriesBase import SlowTimeSeriesBase
from WITecSDK.Modules.ActiveSequencer import ActiveSequencer

class SlowTimeSeriesTimed(SlowTimeSeriesBase):

    def __init__(self, aCOMParameters: COMParameters):
        super().__init__(aCOMParameters)
        self._intervalCOM = aCOMParameters.GetFloatParameter(self._parampath + "MeasurementInterval")
        
    def Initialize(self, numberOfMeasurements: int, numberOfAccumulations: int, integrationTime: float, interval: float):
        super().Initialize(numberOfMeasurements, numberOfAccumulations, integrationTime)
        self.Interval = interval
        self.setMeasurementModeToTimed()

    @property
    def Interval(self) -> float:
        return self._intervalCOM.GetValue()
    
    @Interval.setter
    def Interval(self, interval: float):
        self._intervalCOM.SetValue(interval)

    def setMeasurementModeToTimed(self):
        self._measurementModeCOM.SetValue(1)