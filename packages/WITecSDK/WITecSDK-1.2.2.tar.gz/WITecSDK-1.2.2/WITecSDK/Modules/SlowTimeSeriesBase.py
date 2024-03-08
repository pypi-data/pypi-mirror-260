from WITecSDK.Parameters import COMParameters, ParameterNotAvailableException
from WITecSDK.Modules.ActiveSequencer import ActiveSequencer
from WITecSDK.Modules.HelperStructs import DataChannelDescription

class SlowSeriesBase:

    _parampath = "UserParameters|SequencerTimeSeriesSlow|"

    def __init__(self, aCOMParameters: COMParameters):
        self._numberOfAccumulationsCOM = aCOMParameters.GetIntParameter(self._parampath + "SpectrumAcquisition|Accumulations")
        self._integrationTimeCOM = aCOMParameters.GetFloatParameter(self._parampath + "SpectrumAcquisition|IntegrationTime")

    @property
    def NumberOfAccumulations(self) -> int:
        return self._numberOfAccumulationsCOM.GetValue()

    @NumberOfAccumulations.setter
    def NumberOfAccumulations(self, numberOfAccumulations: int):
        self._numberOfAccumulationsCOM.SetValue(numberOfAccumulations)

    @property
    def IntegrationTime(self) -> float:
        return self._integrationTimeCOM.GetValue()

    @IntegrationTime.setter
    def IntegrationTime(self, integrationTime: float):
        self._integrationTimeCOM.SetValue(integrationTime)
        

class SlowTimeSeriesBase(SlowSeriesBase):

    _statuspath = "Status|Software|Sequencers|SequencerTimeSeriesSlow|"

    def __init__(self, aCOMParameters: COMParameters):
        super().__init__(aCOMParameters)
        channelpath = "UserParameters|DAQSources|SpectralChannels|"
        self._numberOfMeasurementsCOM = aCOMParameters.GetIntParameter(self._parampath + "AmountOfMeasurements")
        self._measurementModeCOM = aCOMParameters.GetEnumParameter(self._parampath + "MeasurementMode")
        self._startTimeSeriesCOM = aCOMParameters.GetTriggerParameter(self._parampath + "Start")
        self._processScriptCommandCOM = aCOMParameters.GetStringParameter("UserParameters|SequencerProcessScript|CommandLine")
        self._subSequenceCOM = aCOMParameters.GetEnumParameter(self._parampath + "SubSequence|SubSequencerName")
        self._readUserDataCOM = aCOMParameters.GetBoolParameter(self._parampath + "UserData|ReadUserData")
        self._userDataCaptionsCOM = aCOMParameters.GetStringFillStatusParameter(self._statuspath + "UserDataCaptions")
        self._userDataUnitsCOM = aCOMParameters.GetStringFillStatusParameter(self._statuspath + "UserDataUnits")
        self._userDataValuesCOM = aCOMParameters.GetFloatFillStatusParameter(self._statuspath + "UserDataValues")
        self._nextIndexCOM = aCOMParameters.GetIntParameter(self._parampath + "IndexOfNextMeasurement")
        self._showSpectrum1COM = aCOMParameters.GetBoolParameter(channelpath + "SpectralCamera1Data|TimeSeriesSlow|Show")
        self._showSpectrum2COM = None
        self._showSpectrum3COM = None
        try:
            self._showSpectrum2COM = aCOMParameters.GetBoolParameter(channelpath + "SpectralCamera2Data|TimeSeriesSlow|Show")
            self._showSpectrum3COM = aCOMParameters.GetBoolParameter(channelpath + "SpectralCamera3Data|TimeSeriesSlow|Show")
        except ParameterNotAvailableException:
            pass
        except Exception as e:
            raise e

    def Initialize(self, numberOfMeasurements: int, numberOfAccumulations: int, integrationTime: float):
        self.NumberOfMeasurements = numberOfMeasurements
        self.NumberOfAccumulations = numberOfAccumulations
        self.IntegrationTime = integrationTime
        self.UseAutoFocus(False)
        self._readUserDataCOM.SetValue(False)
    
    @property
    def NumberOfMeasurements(self) -> int:
        return self._numberOfMeasurementsCOM.GetValue()
    
    @NumberOfMeasurements.setter
    def NumberOfMeasurements(self, numberOfMeasurements: int):
        self._numberOfMeasurementsCOM.SetValue(numberOfMeasurements)

    def UseAutoFocus(self, aUse: bool):
        if aUse:
            self._processScriptCommandCOM.SetValue("AutoFocus")
            self._subSequenceCOM.SetValue(1)
        else:
            self._subSequenceCOM.SetValue(0)

    def CreateDataChannels(self, dataChannels: list[DataChannelDescription]):
        self._readUserDataCOM.SetValue(True)
        captionlist = [i.Caption for i in dataChannels]
        unitlist = [i.Unit for i in dataChannels]
        self._userDataCaptionsCOM.WriteArray(captionlist)
        self._userDataUnitsCOM.WriteArray(unitlist)

    def WriteDataToDataChannels(self, data: list[float]):
        self._userDataValuesCOM.WriteArray(data)

    @property
    def NextIndex(self) -> int:
        return self._nextIndexCOM.GetValue()
    
    def DeactivateShowSpectrum(self) -> bool:
        self._showSpectrum1COM.SetValue(False)
        if self._showSpectrum2COM is not None:
            self._showSpectrum2COM.SetValue(False)
        if self._showSpectrum3COM is not None:
            self._showSpectrum3COM.SetValue(False)

    def Start(self):
        self._startTimeSeriesCOM.ExecuteTrigger()

    def Stop(self):
        self._activeSequencer.StopActiveSequencer()