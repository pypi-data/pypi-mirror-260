from WITecSDK.Parameters import COMParameters

class FastTimeSeries:

    def __init__(self, aCOMParameters: COMParameters):
        parampath = "UserParameters|SequencerTimeSeriesFast|"
        self._integrationTimeCOM = aCOMParameters.GetFloatParameter(parampath + "IntegrationTime")
        self._measurementsCOM = aCOMParameters.GetIntParameter(parampath + "AmountOfMeasurements")
        self._startFastTimeSeriesCOM = aCOMParameters.GetTriggerParameter(parampath + "Start")

    def Initialize(self, measurements: int, integrationTime: float):
        self.Measurements = measurements
        self.IntegrationTime = integrationTime

    @property
    def Measurements(self) -> int:
        return self._measurementsCOM.GetValue()

    @Measurements.setter
    def Measurements(self, numberMeasurements: int):
        self._measurementsCOM.SetValue(numberMeasurements)

    @property
    def IntegrationTime(self) -> float:
        return self._integrationTimeCOM.GetValue()

    @IntegrationTime.setter
    def IntegrationTime(self, integrationTime: float):
        self._integrationTimeCOM.SetValue(integrationTime)

    def Start(self):
        self._startFastTimeSeriesCOM.ExecuteTrigger()