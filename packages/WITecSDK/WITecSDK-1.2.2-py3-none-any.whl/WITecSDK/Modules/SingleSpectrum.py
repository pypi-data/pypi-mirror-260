from WITecSDK.Parameters import COMParameters, ParameterNotAvailableException

class SingleSpectrumBase:

    _sparampath = "UserParameters|SequencerSingleSpectrum|"

    def __init__(self, aCOMParameters: COMParameters):
        self._integrationTimeCOM = aCOMParameters.GetFloatParameter(self._sparampath + "IntegrationTime")
        self._accumulationsCOM = aCOMParameters.GetIntParameter(self._sparampath + "NrOfAccumulations")

    @property
    def NumberOfAccumulations(self) -> int:
        return self._accumulationsCOM.GetValue()

    @NumberOfAccumulations.setter
    def NumberOfAccumulations(self, numberOfAccumulations: int):
        self._accumulationsCOM.SetValue(numberOfAccumulations)

    @property
    def IntegrationTime(self) -> float:
        return self._integrationTimeCOM.GetValue()
    
    @IntegrationTime.setter
    def IntegrationTime(self, integrationTime: float):
        self._integrationTimeCOM.SetValue(integrationTime)


class SingleSpectrum(SingleSpectrumBase):

    def __init__(self, aCOMParameters: COMParameters):
        super().__init__(aCOMParameters)
        channelpath = "UserParameters|DAQSources|SpectralChannels|"
        self._infiniteAccCOM = aCOMParameters.GetBoolParameter(self._sparampath + "InfiniteAccumulation")
        self._startSingleSpectrumCOM = aCOMParameters.GetTriggerParameter(self._sparampath + "Start")
        self._showSpectrum1COM = aCOMParameters.GetBoolParameter(channelpath + "SpectralCamera1Data|SingleSpectrum|Show")
        self._showSpectrum2COM = None
        self._showSpectrum3COM = None
        try:
            self._showSpectrum2COM = aCOMParameters.GetBoolParameter(channelpath + "SpectralCamera2Data|SingleSpectrum|Show")
            self._showSpectrum3COM = aCOMParameters.GetBoolParameter(channelpath + "SpectralCamera3Data|SingleSpectrum|Show")
        except ParameterNotAvailableException:
            pass
        except Exception as e:
            raise e

    def Initialize(self, numberOfAccumulations: int, integrationTime: float):
        self.NumberOfAccumulations = numberOfAccumulations
        self.IntegrationTime = integrationTime
        self._infiniteAccCOM.SetValue(False)

    def DeactivateShowSpectrum(self) -> bool:
        self._showSpectrum1COM.SetValue(False)
        if self._showSpectrum2COM is not None:
            self._showSpectrum2COM.SetValue(False)
        if self._showSpectrum3COM is not None:
            self._showSpectrum3COM.SetValue(False)
    
    def Start(self):
        self._startSingleSpectrumCOM.ExecuteTrigger()