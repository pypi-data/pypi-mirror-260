from WITecSDK.Parameters import COMParameters, ParameterNotAvailableException
from WITecSDK.Modules.BeamPath import BaseDevice, AutomatedCoupler
from WITecSDK.Modules.ActiveSequencer import ActiveSequencer
from WITecSDK.Modules.SlowTimeSeriesBase import SlowSeriesBase

class Polarization:

    def __init__(self, aCOMParameters: COMParameters):
        parampath = "MultiComm|MicroscopeControl|OpticControl|"
        self.Polarizer = Polarizer(aCOMParameters, parampath)
        self.Analyzer = Analyzer(aCOMParameters, parampath)
        self.Syncron = Syncron(aCOMParameters, parampath)
        self.Lambda4 = Lambda4(aCOMParameters, parampath)
        self.Series = PolarizationSeries(aCOMParameters)


class Polarizer(BaseDevice):
    def __new__(cls, aCOMParameters: COMParameters, parampath: str):   
        polarizerInstance = super().__new__(cls, aCOMParameters.GetFloatParameter, parampath + "Selected|Polarizer")
        if polarizerInstance is not None:
            polarizerInstance.__init__(aCOMParameters, parampath)
        return polarizerInstance
            
    def __init__(self, aCOMParameters: COMParameters, parampath: str):
        self._polarizerCOM = self._initCOM
        self._isPolarizerSelectedCOM = aCOMParameters.GetBoolParameter(parampath + "Selected|IsPolarizerSelected")
        
    @property
    def Angle(self) -> float:
        return self._polarizerCOM.GetValue()

    @Angle.setter
    def Angle(self, value: float):
        self._polarizerCOM.SetValue(value)

    @property
    def IsSelected(self) -> bool:
        return self._isPolarizerSelectedCOM.GetValue()


class Analyzer(BaseDevice):
    def __new__(cls, aCOMParameters: COMParameters, parampath: str):   
        analyzerInstance = super().__new__(cls, aCOMParameters.GetFloatParameter, parampath + "Analyzer")
        if analyzerInstance is not None:
            analyzerInstance.__init__(aCOMParameters, parampath)
        return analyzerInstance
            
    def __init__(self, aCOMParameters: COMParameters, parampath: str):
        self._analyzerCOM = self._initCOM
        self.AnalyzerCoupler = AutomatedCoupler(aCOMParameters, parampath + "AnalyzerCoupler")

    @property
    def Angle(self) -> float:
        return self._analyzerCOM.GetValue()

    @Angle.setter
    def Angle(self, value: float):
        self._analyzerCOM.SetValue(value)


class Syncron(BaseDevice):
    def __new__(cls, aCOMParameters: COMParameters, parampath: str):   
        syncronInstance = super().__new__(cls, aCOMParameters.GetFloatParameter, parampath + "AnalyzerPolarizerMovingSynchron")
        if syncronInstance is not None:
            syncronInstance.__init__(aCOMParameters, parampath)
        return syncronInstance
            
    def __init__(self, aCOMParameters: COMParameters, parampath: str):
        self._anaPolSynchronCOM = self._initCOM
        self._anaPolAngleDifferenceCOM = aCOMParameters.GetFloatParameter(parampath + "AnalyzerPolarizerAngleDifference")

    @property
    def Enabled(self) -> bool:
        return self._anaPolSynchronCOM.GetValue()

    @Enabled.setter
    def Enabled(self, value: bool):
        self._anaPolSynchronCOM.SetValue(value)

    @property
    def AngleDifference(self) -> float:
        return self._anaPolAngleDifferenceCOM.GetValue()

    @AngleDifference.setter
    def AngleDifference(self, value: float):
        self._anaPolAngleDifferenceCOM.SetValue(value)


class Lambda4(BaseDevice):
    def __new__(cls, aCOMParameters: COMParameters, parampath: str):   
        lambda4Instance = super().__new__(cls, aCOMParameters.GetFloatParameter, parampath + "Selected|PolarizerIsLambda4Coupled")
        if lambda4Instance is not None:
            lambda4Instance.__init__(aCOMParameters, parampath)
        return lambda4Instance
            
    def __init__(self, aCOMParameters: COMParameters, parampath: str):
        self._isPolarizerLambda4COM = self._initCOM
        self._polarizerLambda4ModeCOM = aCOMParameters.GetEnumParameter(parampath + "Selected|PolarizerLambda4Mode")
    
    @property
    def Enabled(self) -> bool:
        return self._isPolarizerLambda4COM.GetValue()
    
    @property
    def Mode(self) -> int:
        return self._polarizerLambda4ModeCOM.GetValue()

    @Mode.setter
    def Mode(self, unit: int):
        self._polarizerLambda4ModeCOM.SetValue(unit)

    def GetModes(self) -> dict:
        return self._polarizerLambda4ModeCOM.GetAvailableValues()


class PolarizationSeries(SlowSeriesBase):

    def __init__(self, aCOMParameters: COMParameters):
        super().__init__(aCOMParameters)
        self._numberOfPolarizerValuesCOM = aCOMParameters.GetIntParameter(self._parampath + "PolarizerSeries|NumberOfPolarizerValues")
        self._startPolarizerSeriesCOM = aCOMParameters.GetTriggerParameter(self._parampath + "PolarizerSeries|StartPolarizerSeries")
        self._numberOfAnalyzerValuesCOM = aCOMParameters.GetIntParameter(self._parampath + "AnalyzerSeries|NumberOfAnalyzerValues")
        self._startAnalyzerSeriesCOM = aCOMParameters.GetTriggerParameter(self._parampath + "AnalyzerSeries|StartAnalyzerSeries")

    @property
    def StepsPolarizerSeries(self) -> int:
        return self._numberOfPolarizerValuesCOM.GetValue()

    @StepsPolarizerSeries.setter
    def StepsPolarizerSeries(self, value: int):
        self._numberOfPolarizerValuesCOM.SetValue(value)

    @property
    def StepsAnalyzerSeries(self) -> int:
        return self._numberOfAnalyzerValuesCOM.GetValue()

    @StepsAnalyzerSeries.setter
    def StepsAnalyzerSeries(self, value: int):
        self._numberOfAnalyzerValuesCOM.SetValue(value)

    def StartPolarizerSeries(self):
        self._startPolarizerSeriesCOM.ExecuteTrigger()

    def StartAnalyzerSeries(self):
        self._startAnalyzerSeriesCOM.ExecuteTrigger()