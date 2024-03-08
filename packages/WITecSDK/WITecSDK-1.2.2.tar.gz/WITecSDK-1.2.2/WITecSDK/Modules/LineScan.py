"""Module containing the classes for the Line Scan"""

from WITecSDK.Parameters import COMParameters
from WITecSDK.Modules.SingleSpectrum import SingleSpectrumBase
from WITecSDK.Modules.HelperStructs import XYZPosition

class LineScan(SingleSpectrumBase):
    """Base class for Line Scan"""

    _parampath = "UserParameters|SequencerScanLine|"

    def __init__(self, aCOMParameters: COMParameters):
        super().__init__(aCOMParameters)
        self._numberPointsCOM = aCOMParameters.GetIntParameter(self._parampath + "SamplePoints")
        self._startLineScanCOM = aCOMParameters.GetTriggerParameter(self._parampath + "Start")
        self._startXCOM = aCOMParameters.GetFloatParameter(self._parampath + "StartPoint|X")
        self._startYCOM = aCOMParameters.GetFloatParameter(self._parampath + "StartPoint|Y")
        self._startZCOM = aCOMParameters.GetFloatParameter(self._parampath + "StartPoint|Z")
        self._endXCOM = aCOMParameters.GetFloatParameter(self._parampath + "EndPoint|X")
        self._endYCOM = aCOMParameters.GetFloatParameter(self._parampath + "EndPoint|Y")
        self._endZCOM = aCOMParameters.GetFloatParameter(self._parampath + "EndPoint|Z")

    def Initialize(self, numberPoints: int, startPoint: XYZPosition, endPoint: XYZPosition, integrationTime: float, numberOfAccumulations: int):
        self.NumberPoints = numberPoints
        self.StartPoint = startPoint
        self.EndPoint = endPoint
        self.NumberOfAccumulations = numberOfAccumulations
        self.IntegrationTime = integrationTime

    @property
    def NumberOfPoints(self) -> int:
        return self._numberPointsCOM.GetValue()
    
    @NumberOfPoints.setter
    def NumberOfPoints(self, numberOfPoints: int):
        self._numberPointsCOM.SetValue(numberOfPoints)

    @property
    def StartPoint(self) -> XYZPosition:
        return XYZPosition(self._startXCOM.GetValue(), self._startYCOM.GetValue(), self._startZCOM.GetValue())

    @StartPoint.setter
    def StartPoint(self, startPoint: XYZPosition):
        self._startXCOM.SetValue(startPoint.X)
        self._startYCOM.SetValue(startPoint.Y)
        self._startZCOM.SetValue(startPoint.Z)
        
    @property
    def EndPoint(self) -> XYZPosition:
        return XYZPosition(self._endXCOM.GetValue(), self._endYCOM.GetValue(), self._endZCOM.GetValue())

    @EndPoint.setter
    def EndPoint(self, endPoint: XYZPosition):
        self._endXCOM.SetValue(endPoint.X)
        self._endYCOM.SetValue(endPoint.Y)
        self._endZCOM.SetValue(endPoint.Z)

    def Start(self):
        self._startLineScanCOM.ExecuteTrigger()


class LineScan62(LineScan):
    """for Line Scan since 6.2"""
    
    def __init__(self, aCOMParameters: COMParameters):
        super().__init__(aCOMParameters)
        self._integrationTimeCOM = aCOMParameters.GetFloatParameter(self._parampath + "IntegrationTime")
        self._accumulationsCOM = aCOMParameters.GetIntParameter(self._parampath + "NrOfAccumulations")
        self._startCurrentCOM = aCOMParameters.GetTriggerParameter(self._parampath + "StartAtCurrentPosition")
        self._centerCurrentCOM = aCOMParameters.GetTriggerParameter(self._parampath + "CenterAtCurrentPosition")
        self._endCurrentCOM = aCOMParameters.GetTriggerParameter(self._parampath + "EndAtCurrentPosition")
    
    def Initialize(self, numberPoints: int, startPoint: XYZPosition, endPoint: XYZPosition, integrationTime: float, numberOfAccumulations: int):
        self._initializePoints(numberPoints, startPoint, endPoint)
        self.IntegrationTime = integrationTime
        self.NumberOfAccumulations = numberOfAccumulations

    @property
    def IntegrationTime(self) -> float:
        return self._integrationTimeCOM.GetValue()
    
    @IntegrationTime.setter
    def IntegrationTime(self, value: float):
        self._integrationTimeCOM.SetValue(value)

    @property
    def NumberOfAccumulations(self) -> int:
        return self._accumulationsCOM.GetValue()
    
    @NumberOfAccumulations.setter
    def NumberOfAccumulations(self, value: int):
        self._accumulationsCOM.SetValue(value)

    def StartAtCurrentPosition(self):
        self._startCurrentCOM.ExecuteTrigger()

    def CenterAtCurrentPosition(self):
        self._centerCurrentCOM.ExecuteTrigger()

    def EndAtCurrentPosition(self):
        self._endCurrentCOM.ExecuteTrigger()